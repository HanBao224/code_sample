package com.company;

import java.util.ArrayList;

// QUESTION 3:
// find all the points in the data set that are within r from a point p
// Method: construct a tree for abs(x[...]-p)
// find the node which separates nodes <r and >r


public class distance_query{
    private ArrayList<Integer> result;

    public ArrayList<Integer> dis_query(int p, int r, int[] x){
        KD_Tree tree = new KD_Tree(x[0]-p);

        for(int i = 1; i < x.length; i++){
            tree.insert(x[i] - p);
        }

        System.out.println("print the tree in Question3");
        KD_Tree.print_tree(tree.root);

        result = new ArrayList<Integer>();
        dis_query_assit(p, r, tree.root);
        return result;
    }

    public void dis_query_assit(int p, int r, TreeNode root){
        if (root == null) {
            return;
        }
        if (root.value >= -r) {
            dis_query_assit(p, r, root.left);
        }
        if (root.value >= -r && root.value <= r) {
            result.add(root.value + p);
        }
        if (root.value <= r) {
            dis_query_assit(p, r, root.right);
        }
    }
}
