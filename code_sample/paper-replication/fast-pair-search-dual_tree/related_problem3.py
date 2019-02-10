import dual_tree
from sklearn.neighbors import NearestNeighbors
import numpy as np
import bound

from sklearn.neighbors import KernelDensity

# ---------- Required Implementation 3:----------------
# 3. make some improvement
#  A. make a balanced kd-tree would make this algorithm better？
#     KDtrees in this problem are not very unbalanced.
#  B. determine a proper bandwidth.
#  C. in some settings, KNN would work. However, we can't control the outcome.
#  (data points are close to each other, dimension equals number of neighbors?)


def run_improved():
    # run in terminal by using cProfile:
    # python_ml3.6 -m cProfile related_problem3.py
    # 312820 function calls(306104 primitive calls) in 0.497 seconds

    np.random.seed(0)
    data = np.random.rand(1000, 5)
    query_data = np.random.rand(100, 5)
    d = 5

    nbrs = NearestNeighbors(n_neighbors=d, algorithm='kd_tree').fit(data)
    # nbrs = NearestNeighbors(n_neighbors=d, algorithm='ball_tree').fit(data)
    distances, indices = nbrs.kneighbors(query_data)

    prob = []
    for i in range(distances.shape[0]):
        prob.append(bound.gaussian_density(distances[i, :], 1))
    return prob


def run_original():
    # run in terminal by using cProfile:
    # 43683429 function calls(43675324 primitive calls) in 90.51 seconds

    np.random.seed(0)
    data = np.random.rand(1000, 5)
    query_data = np.random.rand(100, 5)

    tree = dual_tree.KDTree(data, leafsize=2)
    treep = dual_tree.KDTree(query_data, leafsize=2)

    dens = dual_tree.KDTree.query_dual_tree(tree, treep, 1, eps=0.001)
    return dens

if __name__ == "__main__":
    dens1 = run_improved()
    dens2 = run_original()
    diff = np.sum((dens1-dens2)*(dens1-dens2))
    print(diff)  # 0.0004
