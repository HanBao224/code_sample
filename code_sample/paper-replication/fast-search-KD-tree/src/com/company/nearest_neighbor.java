package com.company;
import java.util.ArrayList;
import java.util.Arrays;

public class nearest_neighbor {

    private ArrayList result;

    public ArrayList<Integer> nearest_neighbor(int p, int k, int r_max, int[] x) {
        KD_Tree tree = new KD_Tree(x[0] - p);
        for (int i = 1; i < x.length; i++) {
            tree.insert(x[i] - p);
        }

        System.out.println("print the tree in Question4");
        KD_Tree.print_tree(tree.root);

        result = new Arrays();
        nn_assit(p, r_max, tree.root);
        result.sort(Comparator.comparingInt());

        int[] result2 = new int[result.size()];
        for(int i = 0; i < result.size(); i++){
           String temp = result.get(i).toString();
           result2[i] = Integer.parseInt(temp);
        }

        return result;
    }

    public void nn_assit(int p, int r, TreeNode root) {
        if (root == null) {
            return;
        }
        if (root.value >= -r) {
            nn_assit(p, r, root.left);
        }
        if (root.value >= -r && root.value <= r) {
            result.add(root.value + p);
        }
        if (root.value <= r) {
            nn_assit(p, r, root.right);
        }
    }
}