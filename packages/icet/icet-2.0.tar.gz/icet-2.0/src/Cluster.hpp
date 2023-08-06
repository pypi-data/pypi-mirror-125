#pragma once

#include <boost/functional/hash.hpp>
#include "FloatType.hpp"
#include "Geometry.hpp"
#include "LatticeSite.hpp"
#include "Structure.hpp"

using boost::hash;
using boost::hash_combine;

/// This class handles information pertaining to a single cluster.
class Cluster
{
public:

    // Empty constructor
    Cluster() { }

    /// Creates cluster from a structure and a set of lattice sites.
    Cluster(const Structure &structure,
            const std::vector<LatticeSite> &latticeSites);

    /// Returns the order (i.e., the number of sites) of the cluster.
    unsigned int order() const { return _order; }

    /// Returns the radius of the cluster.
    double radius() const { return _radius; }

    /// Returns distances between points in the cluster.
    std::vector<double> distances() const { return _distances; }

private:

    /// List of distances between points in cluster.
    std::vector<double> _distances;

    /// Cluster radius.
    double _radius;

    /// Cluster order (i.e., is it a singlet (1), pair (2), triplet(3), etc.)
    size_t _order;
};
