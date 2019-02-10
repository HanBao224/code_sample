import unittest
from dual_tree import KDTree
import numpy as np
from sklearn.neighbors import KernelDensity

# test 7 functions in dual_tree.py

class TestStringMethods(unittest.TestCase):
    np.random.seed(0)

    # Test build function
    def test_LeafNode(self):
        data = np.array([[0, 2]])
        tree = KDTree(data, leafsize=2)
        # Test if the node is recognized as leaf by the build function.
        self.assertEqual(0, tree.root.idx)
        self.assertSequenceEqual(list([0, 2]), list(tree.root.mins))
        self.assertSequenceEqual(list([0, 2]), list(tree.root.maxes))
        # Test if the information contained by the leaf node is correct.
        self.assertEqual(1, len(tree.children(tree.root)))
        self.assertEqual(0, tree.children(tree.root)[0].idx)
        self.assertEqual(True, isinstance(tree.root, KDTree.LeafNode))

    def test_build1(self):
        data = np.array([[0, 2], [0, 3], [0, 4]])
        tree = KDTree(data, leafsize=2)
        # test if the node is built correctly.
        self.assertSequenceEqual(list([0, 1, 2]), list(tree.root.idx))
        self.assertSequenceEqual(list([0, 2]), list(tree.root.mins))
        self.assertSequenceEqual(list([0, 4]), list(tree.root.maxes))
        # Test if the information contained by the leaf node is correct.
        self.assertSequenceEqual(list([0, 1]), list(tree.children(tree.root)[0].idx))
        self.assertSequenceEqual(list([2]), list(tree.children(tree.root)[1].idx))

    def test_build2(self):
        data = np.array([[1, 1, 2],
                         [0, 1, 2],
                         [3, 1, 2],
                         [3, 2, 1],
                         [3, 3, 4],
                         [3, 1, 3],
                         [2, 3, 1],
                         [3, 4, 1],
                         [3, 1, 0],
                         [3, 4, 5]])
        tree = KDTree(data, leafsize=3)
        # test if the node is built correctly on multi-dimensions.
        self.assertSequenceEqual(list([0, 1, 0]), list(tree.root.mins))
        self.assertSequenceEqual(list([3, 4, 5]), list(tree.root.maxes))

        # split = 2.5; dimension = 3
        # test if the left bound and right bound overlap
        self.assertSequenceEqual(list([0, 1, 2, 3, 6, 7, 8]), list(tree.root.leftchild.idx))
        self.assertSequenceEqual(list([4, 5, 9]), list(tree.root.rightchild.idx))

        # show that after splitting, we still can use .idx to trace the value of the node
        self.assertSequenceEqual(list([2, 3, 6, 7, 8]), list(tree.root.leftchild.rightchild.idx))
        self.assertSequenceEqual(list([0, 1]), list(tree.root.leftchild.leftchild.idx))

        # test if leave size == 3. root.greater shall be a LeafNode
        self.assertTrue(isinstance(tree.root.rightchild, KDTree.LeafNode))

    # Test dual tree algorithm.
    # Test if the answer given by our function is the same as that provided by external libraries.
    def test_query_dual(self):
        data = np.array([[1, 1]])
        pts = np.array([[1, 1]])

        tree = KDTree(data, leafsize=2)
        treep = KDTree(pts, leafsize=2)

        dens = KDTree.query_dual_tree(tree, treep, 1)
        kfit = KernelDensity(bandwidth=1.0, kernel="gaussian",
                             breadth_first=True, leaf_size=2, metric_params=None).fit(data)
        result = kfit.score_samples(pts)
        self.assertTrue((dens - np.exp(result)) < 0.001)

    # random test for dual tree algorithm
    def test_query_dual_rand(self):
        d = 5
        data = np.random.rand(51, d)
        pts = np.random.rand(3, d)

        tree = KDTree(data, leafsize=4)
        treep = KDTree(pts, leafsize=4)

        dens = KDTree.query_dual_tree(tree, treep, 1)
        kfit = KernelDensity(bandwidth=1.0, kernel="gaussian",
                             breadth_first=True, leaf_size=2, metric_params=None).fit(data)
        result = kfit.score_samples(pts)
        self.assertTrue(np.sum(dens - np.exp(result)) < 0.001)

    # test if u, l value are correctly added to each node.
    def test_traverse_add(self):
        data = np.array([[0, 2], [0, 3], [0, 4]])
        tree = KDTree(data, leafsize=1)
        lower = np.zeros(3)
        upper = np.zeros(3)
        l = 0.1
        u = 0.2
        tree.traverse_add(tree.root, lower, upper, l, u)
        self.assertSequenceEqual(list([0.1, 0.1, 0.1]), list(lower))
        self.assertSequenceEqual(list([0.2, 0.2, 0.2]), list(upper))

    # test if the estimated density for nodes in leaf is correct.
    def test_kdebase(self):
        data = np.array([[0, 2]])
        tree = KDTree(data, leafsize=2)

        query = np.array([[0, 2]])
        tree_query = KDTree(query, leafsize=2)
        result = tree.kdebase(tree.root, tree_query.root, tree_query, 1)
        self.assertEqual([0.1592], round(result[0], 4))

    # test if the function return the correct children for one node.
    def test_children(self):
        # LeafNode case
        data = np.array([[0, 2]])
        tree = KDTree(data, leafsize=2)
        self.assertEqual(tree.children(tree.root)[0], tree.root)

        # node case
        data = np.array([[0, 2], [0, 3]])
        tree = KDTree(data, leafsize=1)
        self.assertEqual(tree.children(tree.root)[0].idx, [0])
        self.assertEqual(tree.children(tree.root)[1].idx, [1])

    # test if priority value is calculated correctly.
    def test_priority(self):
        data = np.array([[0, 2], [0, 3]])
        tree = KDTree(data, leafsize=1)
        priority = tree.priority(tree.root, 0.1, 0.2)  # 0.1 * 2 + 0.0001 * random(0, 1)
        self.assertTrue((priority - 0.2) < 0.001)

    # test if the traverse result is correct.
    def test_traverse(self):
        data = np.array([[0, 2], [0, 3]])
        tree = KDTree(data, leafsize=1)
        result = []
        tree.traverse(tree.root, result)  # result = array([0, 1])
        self.assertSequenceEqual(list(result[0]), list([0, 1]))


if __name__ == '__main__':
    unittest.main()

