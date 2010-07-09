"""
Testing for Clustering methods

"""

import numpy as np
from scikits.learn.clustering import AffinityPropagation, \
                        affinity_propagation, MeanShift, meanshift
from numpy.testing import *

# ========================
# = Generate sample data =
# ========================
np.random.seed(0)

n_points_per_cluster = 20
n_clusters = 3
n_points = n_points_per_cluster*n_clusters
means = np.array([[1,1],[-1,-1],[1,-1]])
std = .4

X = np.empty((0, 2))
for i in range(n_clusters):
    X = np.r_[X, means[i] + std * np.random.randn(n_points_per_cluster, 2)]

def test_meanshift():
    """
    MeanShift algorithm

    """
    bandwidth = 1.2

    ms = MeanShift(bandwidth=bandwidth)
    labels = ms.fit(X).labels
    cluster_centers = ms.cluster_centers
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    assert_equal(n_clusters_, n_clusters)

    cluster_centers, labels = meanshift(X, bandwidth=bandwidth)
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    assert_equal(n_clusters_, n_clusters)

def test_affinity_propagation():
    """
    Affinity Propagation algorithm

    """

    # ========================
    # = Compute similarities =
    # ========================
    X_norms = np.sum(X*X, axis=1)
    S = - X_norms[:,np.newaxis] - X_norms[np.newaxis,:] + 2 * np.dot(X, X.T)
    p = 10*np.median(S)

    # ================================
    # = Compute Affinity Propagation =
    # ================================

    labels = affinity_propagation(S, p)

    unique_labels = np.unique(labels)
    n_clusters_ = unique_labels.size

    assert_equal(n_clusters, n_clusters_)

    af = AffinityPropagation()
    labels = af.fit(S, p).labels

    unique_labels = np.unique(labels)
    n_clusters_ = unique_labels.size

    assert_equal(n_clusters, n_clusters_)
