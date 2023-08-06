#include "ClusterExpansionCalculator.hpp"
#include <pybind11/stl.h>

ClusterExpansionCalculator::ClusterExpansionCalculator(const ClusterSpace &clusterSpace,
                                                       const Structure &structure,
                                                       const double fractionalPositionTolerance)
{
    _clusterSpace = clusterSpace;
    _supercell = structure;
    LocalOrbitListGenerator LOLG = LocalOrbitListGenerator(clusterSpace.getPrimitiveOrbitList(), _supercell, fractionalPositionTolerance);
    size_t uniqueOffsets = LOLG.getNumberOfUniqueOffsets();
    int numberOfOrbits = _clusterSpace.getPrimitiveOrbitList().size();
    std::vector<Orbit> orbitVector;
    _fullOrbitList = LOLG.getFullOrbitList();

    // Set equivalent cluster equal to the permuted clusters so no permutation is required in the orbit list counting.
    for (auto &orbit : _fullOrbitList._orbits)
    {
        auto permutedClusters = orbit.getPermutedEquivalentClusters();
        orbit.setEquivalentClusters(permutedClusters);
    }

    for (const auto orbit : clusterSpace.getPrimitiveOrbitList().getOrbits())
    {
        orbitVector.push_back(Orbit(orbit.getRepresentativeCluster()));
    }

    // Permutations for the clusters in the orbits
    std::vector<std::vector<std::vector<int>>> permutations(numberOfOrbits);

    /* Strategy for constructing the "full" primitive orbit lists.

    First we fill up a `std::vector<Orbit> orbitVector`,
    where `vector<orbit>` is essentially an orbit list.

    The existing method for constructing the _full_ orbit list proceeds
    by looping over all local orbit lists with `LocalOrbitListGenerator` and
    adding the sites to the local orbit list.

    Now we do something similar by looping over each local orbit list
    (by looping over `offsetIndex`).
    The local orbitlist is retrieved here:
        `LOLG.getLocalOrbitList(offsetIndex).getOrbits()`

    Then for each orbit `orbitIndex` in `LOLG.getLocalOrbitList(offsetIndex).getOrbits()`
    each group of lattice sites in `orbit.equivalentSites()` is added to
    `orbitVector[orbitIndex]` if the lattice sites have a site with offset `[0, 0, 0]`.

    When the full primitive orbit list is used to create a local orbit list for
    site `index` in the supercell it should thus contain all lattice sites that
    contain `index`.
    */

    for (size_t offsetIndex = 0; offsetIndex < uniqueOffsets; offsetIndex++)
    {
        int orbitIndex = -1;
        // This orbit is a local orbit related to the supercell
        for (const auto orbit : LOLG.getLocalOrbitList(offsetIndex).getOrbits())
        {
            orbitIndex++;

            auto orbitPermutations = orbit.getPermutationsOfEquivalentClusters();

            int eqSiteIndex = -1;

            for (const auto cluster : orbit.getEquivalentClusters())
            {
                eqSiteIndex++;

                std::vector<LatticeSite> primitiveEquivalentSites;
                for (const auto site : cluster)
                {
                    Vector3d sitePosition = _supercell.getPosition(site);
                    auto primitiveSite = _clusterSpace.getPrimitiveStructure().findLatticeSiteByPosition(sitePosition, fractionalPositionTolerance);
                    primitiveEquivalentSites.push_back(primitiveSite);
                }
                std::vector<std::vector<LatticeSite>> translatedClusters = _clusterSpace.getPrimitiveOrbitList().getSitesTranslatedToUnitcell(primitiveEquivalentSites, false);

                for (auto translatedCluster : translatedClusters)
                {
                    if (std::any_of(translatedCluster.begin(), translatedCluster.end(), [=](LatticeSite ls)
                                    { return (ls.unitcellOffset()).norm() < fractionalPositionTolerance; }))
                    {
                        // false or true here does not seem to matter
                        if (!orbitVector[orbitIndex].contains(translatedCluster, true))
                        {
                            orbitVector[orbitIndex].addEquivalentCluster(translatedCluster);
                            permutations[orbitIndex].push_back(orbitPermutations[eqSiteIndex]);
                        }
                    }
                }
            }
        }
    }

    // Now create the full primitive orbit list using the vector<orbit>
    _fullPrimitiveOrbitList.setPrimitiveStructure(_clusterSpace.getPrimitiveStructure());
    int orbitIndex = -1;
    for (auto orbit : orbitVector)
    {
        orbitIndex++;
        orbit.setPermutationsOfEquivalentClusters(permutations[orbitIndex]);
        _fullPrimitiveOrbitList.addOrbit(orbit);
    }

    // Calculate the permutation for each orbit in this orbit list.
    // This is normally done in the constructor but since we made one manually
    // we have to do this ourself.
    // _fullPrimitiveOrbitList.addPermutationInformationToOrbits(_clusterSpace.getOrbitList().getFirstColumnOfMatrixOfEquivalentSites(),
    //                                                           _clusterSpace.getOrbitList().getMatrixOfEquivalentSites());

    _primToSupercellMap.clear();
    _indexToOffset.clear();

    // Precompute all possible local orbitlists for this supercell and map it to the offset
    for (size_t i = 0; i < structure.size(); i++)
    {
        Vector3d localPosition = structure.getPositions().row(i);
        LatticeSite localSite = _clusterSpace.getPrimitiveStructure().findLatticeSiteByPosition(localPosition, fractionalPositionTolerance);
        Vector3d offsetVector = localSite.unitcellOffset();
        _indexToOffset[i] = offsetVector;

        if (_localOrbitlists.find(offsetVector) == _localOrbitlists.end())
        {
            _localOrbitlists[offsetVector] = _fullPrimitiveOrbitList.getLocalOrbitList(structure, offsetVector, _primToSupercellMap, fractionalPositionTolerance);

            // Set equivalent cluster equal to the permuted clusters so no permutation is required in the orbit list counting.
            for (auto &orbit : _localOrbitlists[offsetVector]._orbits)
            {
                auto permutedClusters = orbit.getPermutedEquivalentClusters();
                orbit.setEquivalentClusters(permutedClusters);
            }
        }
    }
}

/**
@details Calculate change in cluster vector upon change in occupation on one site
@param occupationsBefore the occupation vector for the supercell before the flip
@param flipIndex the index in the supercell where occupation has changed
@param newOccupation new atomic number on site index
*/
std::vector<double> ClusterExpansionCalculator::getClusterVectorChange(const py::array_t<int> &occupationsBefore,
                                                                       int flipIndex,
                                                                       int newOccupation)
{
    if (occupationsBefore.size() != _supercell.size())
    {
        throw std::runtime_error("Input occupations and internal supercell structure mismatch in size (ClusterExpansionCalculator::getClusterVectorChange)");
    }
    _supercell.setAtomicNumbers(occupationsBefore);

    if (flipIndex >= _supercell.size())
    {
        throw std::runtime_error("flipIndex larger than the length of the structure (ClusterExpansionCalculator::getClusterVectorChange)");
    }

    // The first element in the cluster vector (difference) should be zero (because we take 1 - 1)
    double firstElement = 0.0;

    return _clusterSpace.occupyClusterVector(_localOrbitlists[_indexToOffset[flipIndex]], _supercell, firstElement, flipIndex, newOccupation);
}

/**
@details This constructs a cluster vector that only includes clusters that contain the input index.
@param occupations the occupation vector for the supercell
@param index the local index of the supercell
*/
std::vector<double> ClusterExpansionCalculator::getLocalClusterVector(const py::array_t<int> &occupations, int index)
{

    if (occupations.size() != _supercell.size())
    {
        throw std::runtime_error("Input occupations and internal supercell structure mismatch in size (ClusterExpansionCalculator::getLocalClusterVector)");
    }
    _supercell.setAtomicNumbers(occupations);

    // The first element can be thought of as shared between all sites when constructing a local orbit list
    double firstElement = 1.0 / _supercell.size();

    return _clusterSpace.occupyClusterVector(_localOrbitlists[_indexToOffset[index]], _supercell, firstElement, index);
}

/**
@details Calculate the cluster vector for a supercell.
@param occupations the occupation vector of the supercell
*/
std::vector<double> ClusterExpansionCalculator::getClusterVector(const py::array_t<int> &occupations)
{
    if (occupations.size() != _supercell.size())
    {
        throw std::runtime_error("Input occupations and internal supercell structure mismatch in size (ClusterExpansionCalculator::getClusterVector)");
    }
    _supercell.setAtomicNumbers(occupations);

    return _clusterSpace.occupyClusterVector(_fullOrbitList, _supercell);
}
