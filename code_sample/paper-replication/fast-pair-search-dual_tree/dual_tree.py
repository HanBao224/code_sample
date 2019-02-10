import numpy as np
import heapq
import bound

class KDTree:
    """
    Construct a KDTree. It contains two different kinds of nodes: nodes and leafnodes.
    Leafnodes will not be split or sequenced. All points in the subtree with a smaller
    value than the node will appear in the left subtree and all points with larger value
    will be in the right subtree.

    Parameters:
    data: array, with n lines and m columns.
    leafsize: positive integer.

    Methods:
    build: build a kd-tree, root and tree data are maintained.
           root will be linked with its greater/left children.
           Each node has two values: maxes and mins,
           which represents the max/min bound of the nodes it contains.
           maxes/mins is the max/min values in all the dimensions.
           Each node is linked with the data array by memorizing the indexs of all the data in its bound.

    query_dual_tree: return density estimation for all the nodes in another KDTree.
           1) if the difference is tolerable, the average of upper and lower would be the estimation
           for all the nodes in q's bound.
           2) if the query node and data node are leafnode. compute all the density contribution and sum them.
           3) else compute the density bound between the children of query node and data node.
           until the diff is tolerable or both tree reaches leafnodes.

    Usage: data = np.random.rand(100, 5)
           tree = dual_tree.KDTree(data, leafsize=2)
    """

    def __init__(self, data, leafsize):
        """
        :param data: array, with n lines and m columns.
        :param leafsize: The size of the leaf.
                         Leafnodes will not be split or sequenced.
        :param maxes: upper bound array. The biggest value of each column/dimension owned by the this tree.
        :param mins: lower bound array. The smallest value of each column/dimension owned by the this tree.
        :param root: the root node of the tree, linked with its left and right child
        """
        self.data = np.asarray(data)
        self.n, self.m = np.shape(self.data)
        self.leafsize = leafsize
        self.maxes = np.amax(self.data, axis=0)
        self.mins = np.amin(self.data, axis=0)
        self.root = self.build(np.arange(self.n), self.maxes, self.mins)

    # split value, dimensions and original data are not stored in the node.
    class Node:
        def __init__(self, leftchild, rightchild, idx, mins, maxes):
            """
            :param leftchild:
            :param rightchild:
            :param idx: index of all the children nodes in the bound of current node.
            :param mins: The biggest value of each column/dimension owned by the this tree, array.
            :param maxes: The lower value of each column/dimension owned by the this tree, array.
            """
            self.leftchild = leftchild  # left children
            self.rightchild = rightchild  # right children
            self.idx = idx
            self.mins = mins
            self.maxes = maxes

    # leafnode doesn't have children.
    class LeafNode:
        """
         :param idx: index of all the children nodes in the bound of current node.
         :param mins: The biggest value of each column/dimension owned by the this tree, array.
         :param maxes: The lower value of each column/dimension owned by the this tree, array.
        """
        def __init__(self, idx, mins, maxes):
            self.idx = idx
            self.mins = mins
            self.maxes = maxes

    def build(self, idx, maxes, mins):
        """
        :param idx: position of node's value in the data array.
        :param maxes: biggest value in each dimension (column) in a narray.
        :param mins: smallest value in each dimension (column) in a narray.
        :return: link tree root with other nodes and save some information in the nodes.

        Build a tree:
        1. check if the node is a leaf by using this condition: length("nodes in the bound") <= required leafsize.
        2. If upper bound == lower bound, there is one node left on this branch. It must be a leafnode.
        3. Split the data, data which is smaller than the average of max value and min value on one dimension
           (which has the biggest range) will be included in the left-child node,
           other points would be in right-child node's bound.
        4. If there is no point in left/right node's bound, split the data again based on the median rather than mean.
        5. Repeat, until all the points are linked or stored in the leafnodes.

        This KDTree may not be balanced.
        """
        # boundary condition1: if the node is a leafnode
        if len(idx) <= self.leafsize:
            leafmins = np.amin(self.data[idx], axis=0)
            leafmaxes = np.amax(self.data[idx], axis=0)
            return KDTree.LeafNode(idx, leafmins, leafmaxes)
        else:
            data = self.data[idx]
            # split on the dimension which has the largest range of value
            d = np.argmax(maxes-mins)
            maxval = maxes[d]
            minval = mins[d]

            # boundary condition2: if the upper bound == lower bound
            if maxval == minval:
                return KDTree.LeafNode(idx)

            data = data[:, d]
            split = (maxval + minval)/2

            leftchild_idx = np.nonzero(data <= split)[0]
            rightchild_idx = np.nonzero(data > split)[0]

            # If the dividing method is not proper, points would be split based on median value
            if len(leftchild_idx) == 0 or len(rightchild_idx) == 0:
                split = np.median(data, axis=0)
                leftchild_idx = np.nonzero(data <= split)[0]
                rightchild_idx = np.nonzero(data > split)[0]

            right_mins = np.copy(mins)
            right_mins[d] = split
            left_maxes = np.copy(maxes)
            left_maxes[d] = split

            # Recursion
            node0 = KDTree.Node(self.build(idx[leftchild_idx], left_maxes, mins),
                                self.build(idx[rightchild_idx], maxes, right_mins),
                                idx, mins, maxes)
            return node0

    def query_dual_tree(self, other, h=1, eps=0.0001):
        """
        :param other: KDTree which contains query data.
        :param h: bandwidth.
        :param eps: accepted error rate.
        :return: an array, estimated density for each point in the query array.

        Query_dual_tree: return density estimation for all the nodes in another KDTree.
        1. Get the u, l (upper/lower bound of density y) from upper/lower bound of x (input data)
        2. If the difference between u and l is small enough, let them be the density for all the nodes contained in the bound.
        3. If it is not, calculate the u, l for the children of the current nodes.
           Put the results in a priority queue, repeat 1, 2.
        4. Repeat until we reach the leaf or there is no nodes in the queue.

        """
        P = []  # Priority queue
        lower = np.zeros(other.n)
        upper = np.zeros(other.n)
        Nq = other.n
        heapq.heappush(P, (0, other.root, self.root))

        while P:
            temp, q, d = heapq.heappop(P)
            l, u = bound.find_bound(q, d, h)
            if (u-l) <= 2 * eps * np.min(lower[q.idx]) / Nq:
                lower, upper = self.traverse_add(q, lower, upper, l, u)
            elif isinstance(q, KDTree.LeafNode) and isinstance(d, KDTree.LeafNode):
                prob = self.kdebase(q, d, other, h)
                lower[q.idx] += prob
                upper[q.idx] += prob
            else:
                for qchild in self.children(q):
                    for dchild in self.children(d):
                        priority_index = self.priority(qchild, l, u)
                        heapq.heappush(P, (priority_index, qchild, dchild))
        return (lower+upper)/2

    def traverse_add(self, q, lower, upper, l, u):
        """
        :param q: one node query in the query data tree
        :param lower: maintain lower contribution of each point in the query data tree.
        :param upper: maintain upper contribution of each point in the query data tree.
        :param l: min value of density contribution
        :param u: max value of density contribution
        :return: two array.

        This function will let l, u be the lower and upper contribution value for each nodes in q's box.
        """
        lower[q.idx] = l
        upper[q.idx] = u
        return lower, upper

    def kdebase(self, q, d, other, h):
        """
        :param q: leafnode
        :param d: leafnode
        :param other: query tree
        :param h: bandwidth
        :return: density for a node in q's bound,
                 contributed by all the nodes in d's bound.
        """
        data_in_d = self.data[d.idx, :]
        data_in_q = other.data[q.idx, :]

        colnum_of_d = data_in_d.shape[1]
        rownum_of_q = data_in_q.shape[0]
        rownum_of_d = data_in_d.shape[0]
        result = np.zeros(rownum_of_q)

        H = np.diag((h ** 2) * np.ones(colnum_of_d))

        for i in range(rownum_of_q):
            for j in range(rownum_of_d):
                temp = (np.linalg.inv(H)**(1/2)).dot(data_in_q[i, :] - data_in_d[j, :])
                result[i] += np.linalg.det(H)**(-1/2) * bound.gaussian_density(temp, h) / self.n
        return result

    def children(self, q):
        """
        :param q: input one node
        :return: return its children. Leafnode has no children, then return itself.
        """
        if isinstance(q, KDTree.LeafNode):
            return [q]
        else:
            return [q.leftchild, q.rightchild]

    def priority(self, q, l, u):
        """
        :param q: tree node
        :param l: lower bound of the contribution of all the points in q's bound
        :param u: upper bound of the contribution of all the points in q's bound
        :return: an index used to sort the elements in the priority queue.
        """
        node_num = len(q.idx)
        return node_num * (u-l) + 0.0001 * np.random.uniform(0, 1, size=1)[0]

    def traverse(self, current_node, result):
        """
        traverse all the points contained in the current_node.
        :param current_node: where the traverse process will start.
        :param result: index array, in the order of pre-order traversal method.
        """
        if current_node is None or isinstance(current_node, KDTree.LeafNode):
            return
        result.append(current_node.idx)
        self.traverse(current_node.rightchild, result)
        self.traverse(current_node.leftchild, result)


