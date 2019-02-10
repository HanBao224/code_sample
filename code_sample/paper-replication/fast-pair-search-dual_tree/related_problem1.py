import dual_tree
import numpy as np
import bound
from sklearn import neighbors

# command line: python related_problem1.py

# -------------------- Implementation 1:--------------------
# Dual_tree method produces the same results as naive method.
# Time complexity: Dual_Tree_Query(average): O(N*logN)
# Details:
#                  Build a tree: N*logN. (√)
#                  Priority queue: logN
#                  Binary tree- query one point: logN
#
#                  Query another tree(dual tree algorithm):
#                  Average complexity equals to: Traverse.
#                                                For all bounds where u-l <= 2 * eps * f(Q),
#                                                traverse_add(q, lower, upper, l, u).
#                  => O(N)
#
# Naive KDE: O(k*N^2).
# Dual Tree method is faster than Naive KDE.

# Dual Tree


def naiveKDE(query_data, data):
    # Naive KDE
    NaiveKDE = np.zeros(query_data.shape)

    for i in range(query_data.shape[0]):
        for j in range(data.shape[0]):
            NaiveKDE[i] += bound.gaussian_density(query_data[i] - data[j], 1)

    kde = np.sum(NaiveKDE, axis=1)/(data.shape[0] * data.shape[1] * 1)
    return kde


if __name__ == "__main__":
    np.random.seed(0)
    data = np.random.rand(100, 5)
    query_data = np.random.rand(9, 5)

    tree = dual_tree.KDTree(data, leafsize=2)
    treep = dual_tree.KDTree(query_data, leafsize=2)
    N = np.shape(treep.data)
    n = N[0]

    dens = dual_tree.KDTree.query_dual_tree(tree, treep, 1)
    print("density produced by dual tree", dens)

    # sklearn package
    kfit = neighbors.KernelDensity(bandwidth=1.0, kernel="gaussian",
                                   breadth_first=True, leaf_size=2, metric_params=None).fit(data)
    result = kfit.score_samples(query_data)
    print("kderesult:", np.exp(result))

    kde = naiveKDE(query_data, data)
    print("density produced by naive KDE", kde)

