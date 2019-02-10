import related_problem1
import related_problem2
import related_problem3
import dual_tree
import unittest
import numpy as np


class TestStringMethods(unittest.TestCase):

    # test if naiveKDE works for N*M data
    def test_naiveKDE(self):
        data = np.array([[0, 0], [0, 0]])
        query_data = np.data = np.array([[0, 0], [0, 0]])

        kde = related_problem1.naiveKDE(query_data, data)
        self.assertEqual(0.1592, round(kde[0], 4))
        self.assertEqual(0.1592, round(kde[0], 4))

    # test if implementation 2 can be run
    def test_run_dualtree_query(self):
        error = related_problem2.run_dualtree_query(10)
        self.assertTrue(error < 0.001)
    # test the result produced by ball-tree and
    # whether implementation 3 can be run without Exception

    def test_run_rp3(self):
        dens1 = related_problem3.run_improved()
        dens2 = related_problem3.run_original()
        diff = np.sum((dens1 - dens2) * (dens1 - dens2))
        self.assertTrue(diff < 0.01)

if __name__ == '__main__':
    unittest.main()


