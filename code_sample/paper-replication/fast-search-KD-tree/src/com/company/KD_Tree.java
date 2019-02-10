package com.company;

// QUESTION 1: BUILD A KD_TREE
// The required Kd_tree in the question is actually not a segment tree but a binary-search tree.
// The value of one tree node represents the left margin of the interval (left descendants <= tree value).
// All the right descendants > tree value.

// One thing that needs to be explained:
// I think the condition "left descendants <= tree value" should not be viewed as an 'overlap'.
// If we remove the '=', it would cause much inconvenience in the latter questions.


public class KD_Tree {

    public TreeNode root;

    public KD_Tree(int num){
        root = new TreeNode(num, null, null, null);
    }

    public void insert(int num) {
        TreeNode node = new TreeNode(num, null, null, null);
        TreeNode current;

        if (root == null) {
            root = node;
            return;
        } else {
            current = root;
            while(true) {
                if (num <= current.value) {
                    if (current.right == null) {
                        current.right = node;
                        return;
                    } else {
                        current = current.right;
                    }
                } else {
                    if(current.left == null){
                        current.left = node;
                        return;
                    }else{
                        current = current.left;
                    }
                } // if
            }// while
        }// if
    }

    public static void print_tree(TreeNode current){
        if(current != null){
            System.out.println(current.value);
            print_tree(current.right);
            print_tree(current.left);
        } //  pre_order traversal
    }

    public void inOrder(TreeNode current){
        if(current != null){
            inOrder(current.left);
            System.out.print(" "+current.value);
            inOrder(current.right);
        }
    }

    public void postOrder(TreeNode current){
        if(current != null){
            postOrder(current.left);
            postOrder(current.right);
            System.out.print(" "+current.value);
        }
    }

}
