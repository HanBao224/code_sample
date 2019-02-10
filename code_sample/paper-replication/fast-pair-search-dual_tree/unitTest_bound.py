import unittest
import bound
from dual_tree import KDTree
import numpy as np

# test 3 functions in dual_tree.py


class TestStringMethods(unittest.TestCase):

    # test if we found the correct bound for the data
    def test_find_bound(self):
        query = np.array([[0, 2]])
        tree_query = KDTree(query, leafsize=1)

        data = np.array([[0, 2]])
        tree = KDTree(data, leafsize=1)

        # lower_distance = upper_distance = 0
        l, u = bound.find_bound(tree.root, tree_query.root, 1)
        self.assertEqual([0.1592], round(l, 4))
        self.assertEqual([0.1592], round(u, 4))

        query = np.array([[1, 2]])
        tree_query = KDTree(query, leafsize=1)

        data = np.array([[0, 2]])
        tree = KDTree(data, leafsize=1)
        l, u = bound.find_bound(tree.root, tree_query.root, 1)
        self.assertEqual([0.1592], round(u, 4))

    # test if the change low function works well
    # case1: need not change the distance bound
    def test_if_change_low1(self):
        query = np.array([[1, 2], [3, 4]])
        tree_query = KDTree(query, leafsize=1)

        data = np.array([[0, 2], [3, 4]])
        tree = KDTree(data, leafsize=1)

        self.assertTrue(not bound.if_change_low(tree.root.mins[0], tree.root.maxes[0],
                                            tree_query.root.mins[0], tree_query.root.maxes[0]))
        self.assertTrue(not bound.if_change_low(tree.root.mins[1], tree.root.maxes[1],
                                            tree_query.root.mins[1], tree_query.root.maxes[1]))

    # case2: need to change the distance bound
    def test_if_change_low2(self):
        query = np.array([[5, 6], [10, 11]])
        tree_query = KDTree(query, leafsize=1)

        data = np.array([[0, 2], [3, 4]])
        tree = KDTree(data, leafsize=1)

        self.assertTrue(bound.if_change_low(tree.root.mins[0], tree.root.maxes[0],
                                            tree_query.root.mins[0], tree_query.root.maxes[0]))
        self.assertTrue(bound.if_change_low(tree.root.mins[1], tree.root.maxes[1],
                                            tree_query.root.mins[1], tree_query.root.maxes[1]))

    # test if gaussian density is calculated correctly.
    def test_gaussian_density(self):
        X = np.array([0, 0])
        prob = bound.gaussian_density(X, 1)
        self.assertEqual(0.1592, round(prob, 4))

if __name__ == '__main__':
    unittest.main()
