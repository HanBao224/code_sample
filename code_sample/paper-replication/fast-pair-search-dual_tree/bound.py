import numpy as np
from scipy import stats


def find_bound(q, d, h):
    """
    Calculate the upper and lower bound of density contribution of all the nodes
    in one node's bound on one query node.

    Method: If the bounds of data node(d) and query node(q) are overlap, l = 0
    Otherwise compute the biggest and smallest distance of the two bound and go through gaussian function.

    :param q: node in the query tree
    :param d: node in the data tree
    :param h: bandwidth
    :return: upper and lower density bound
    """
    m = q.maxes.shape[0]
    diff = np.zeros((4, m))
    for i in range(m):
        diff[0, i] = np.abs(q.mins[i]-d.mins[i])
        diff[1, i] = np.abs(q.mins[i]-d.maxes[i])
        diff[2, i] = np.abs(q.maxes[i]-d.mins[i])
        diff[3, i] = np.abs(q.maxes[i]-d.maxes[i])
    upper_dis = diff.max(0)
    lower_dis = diff.min(0)

    for i in range(len(lower_dis)):
        if if_change_low(q.mins[i], q.maxes[i], d.mins[i], d.maxes[i]):
            lower_dis[i] = 0

    upper_des_bound = gaussian_density(lower_dis, h) / h
    lower_des_bound = gaussian_density(upper_dis, h) / h
    return lower_des_bound, upper_des_bound


def if_change_low(mins1, maxes1, mins2, maxes2):
    """
    :param mins1: max value on one dimension
    :param maxes1: min value on one dimension
    :param mins2: max value on one dimension of another node's bound
    :param maxes2: min value on one dimension of another node's bound
    :return: boolean value.

    If maxes is smaller than mins when we combine query node's bound and
    data node's bound together, the lower distance need to be changed to zero.
    This function returns True if the distance bound needs to be changed.
    """
    return min(maxes1, maxes2) <= max(mins1, mins2)


def gaussian_density(X, h):
    """
    :param X: array, distance of two nodes.
    :param h: bandwidth
    :return: corresponding Y calculated by using multi-dimension Gaussian distribution.
    """
    n = X.shape[0]
    H = np.diag((h ** 2) * np.ones(n))
    mu = np.zeros(len(X))
    cov = np.diag(np.ones(len(X)))
    unadjusted_prob = stats.multivariate_normal.pdf((np.linalg.inv(H) ** (1/2)).dot(X), mean=mu, cov=cov)
    prob = np.linalg.det(H)**(-1/2) * unadjusted_prob
    return prob
