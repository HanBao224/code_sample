import dual_tree
import numpy as np

from sklearn.neighbors import KernelDensity

# command line: python related_problem2.py

# ---------- Required Implementation2:----------------------
# 2. How does your performance scale with the number of points
# Use cProfile to get the run time


# Result:
#
# ----------------------------------------------------
# Case1: points in data tree = 1000, query = 11
# In terminal:
# python_ml3.6 -m cProfile related_problem2.py
# total error:
#              2.14298991674e-06
# 2085619 function calls (2078612 primitive calls) in 3.728 seconds

# ----------------------------------------------------
# Case2: points in data tree = 10000, query = 11
# total error:
#              5.35973736943e-06
# 18375218 function calls (18365672 primitive calls) in 31.366 seconds


# ----------------------------------------------------
# Case3: points in data tree = 1000, query = 110
# total error: 4.59396070857e-05
# 16797137 function calls (16790104 primitive calls) in 31.588 seconds


# ----------------------------------------------------
# Case4: points in data tree = 10000, query = 110
# total error:
#              3.46642590995e-05
# 134424919 function calls (134415348 primitive calls) in 270.206 seconds
#
# Conclusion: N2/N1 = 10 times, time2/time1 ≈/< 10 times
#             N4/N1 = 10 times, M4/M1 = 10 times, time4/time1 ≈/< 100 times.

# (because complexity = O(N*logN))

def run_dualtree_query(K):
    np.random.seed(0)
    data = np.random.rand(K, 5)
    query_data = np.random.rand(int(K/10)+1, 5)
    # query_data = np.random.rand(11, 5)/(110, 5)

    tree = dual_tree.KDTree(data, leafsize=10)
    treep = dual_tree.KDTree(query_data, leafsize=10)
    N = np.shape(treep.data)
    n = N[0]

    dens = dual_tree.KDTree.query_dual_tree(tree, treep, 1, n)

    kfit = KernelDensity(bandwidth=1.0, kernel="gaussian",
                         breadth_first=True, leaf_size=2, metric_params=None).fit(data)
    result = kfit.score_samples(query_data)
    return np.sum((dens-np.exp(result))**2)

if __name__ == "__main__":
    error = run_dualtree_query(K=1000)
    # error = run_dualtree_query(K=1000)
