package com.company;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.List;

public class search_pairs {

    public static Map<Integer, List<Integer>> pair_query(TreeNode root, int r) {
        Map<Integer, List<Integer>> result = new HashMap<Integer, List<Integer>>();
        pr_search(root, r, result);
        return result;
    }

    public static void pr_search(TreeNode root, int r, Map<Integer, List<Integer>> result) {
        // for each node, implement it to various nodes.
        if(root == null){
           return;
        }

        List<Integer> temp = new ArrayList<>();
        pr_search_assit(root, root.value, r, temp);
        result.put(root.value, temp);

        pr_search(root.left, r, result);
        pr_search(root.right, r, result);

    }

    public static void pr_search_assit(TreeNode root, int value, int r, List<Integer> temp){
        if(root == null){
            return;
        }
        if( value - root.left.value < r){
            temp.add(root.left.value);
            pr_search_assit(root.left, value, r, temp);
        } else if(root.right.value - value < r){
            temp.add(root.right.value);
            pr_search_assit(root.right, value, r, temp);
        } else if(value - root.left.value > r && root.right.value - value <r){
            temp.add(root.right.value);
            pr_search_assit(root.right, value, r, temp);
        }

    }
}
