// QUESTION 2:

// In java, one can not use functions as arguments.
// I have tried the following methods- using interface is the only way to call a so-call 'callback' function.
// It can work but it doesn't make sense. We use more simple methods to traverse the tree,
// just as what I wrote in KD_tree.

// I decide to pass the assignment2 right now. I will try it later with another language (like C++).


package com.company;
import java.util.ArrayList;

interface Pre_fun{
    public ArrayList<Double> pre_fun(TreeNode start_node, ArrayList<Double> accumulator);
}

interface Mid_fun{
    public ArrayList<Double> mid_fun(TreeNode start_node, ArrayList<Double> accumulator);
}

interface Post_fun{
    public ArrayList<Double> post_fun(TreeNode start_node, ArrayList<Double> accumulator);
}

class traverse_construct {

    public ArrayList<Double> traverse(int[] x, TreeNode start_node, ArrayList<Double> accumulator,
                                      Pre_fun pref, Mid_fun midf, Post_fun postf){

        accumulator = pref.pre_fun(start_node, accumulator);
        accumulator = traverse(x, start_node.left, accumulator, pref, midf, postf);
        accumulator = midf.mid_fun(start_node, accumulator);
        accumulator = traverse(x, start_node.right, accumulator, pref, midf, postf);
        accumulator = postf.post_fun(start_node, accumulator);

        return accumulator;
    }
}


class traversal {

    // Check the bounding boxes of childnodes don't overlap.
    // Methods: check all the node.starts.
    public boolean extension1(int[] x, TreeNode start_node, ArrayList<Double> accumulator,
                           Pre_fun pref, Mid_fun midf, Post_fun postf) {
        traverse_construct tc1 = new traverse_construct();
        tc1.traverse(x, start_node, accumulator, new Pre_fun() {
            @Override
            public ArrayList<Double> pre_fun(TreeNode start_node, ArrayList<Double> accumulator) {
                return accumulator;
            }
        }, new Mid_fun() {
            @Override
            public ArrayList<Double> mid_fun(TreeNode start_node, ArrayList<Double> accumulator) {
                return accumulator;
            }
        }, new Post_fun() {
            @Override
            public ArrayList<Double> post_fun(TreeNode start_node, ArrayList<Double> accumulator) {
                return accumulator;
            }
        });

        if (accumulator.size() < x.length) {
            return false;
        } else {
            return true;
        }

    }
}