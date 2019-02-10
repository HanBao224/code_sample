// provide user control interface

package com.company;
import java.util.ArrayList;
import java.util.Arrays;

public class Main {

    public static void main(String args[]) {
        // write your code here
        int[] temp = new int[args.length];

        for(int i = 0; i < args.length; i++){
            temp[i] = Integer.parseInt(args[i]);
        }

        KD_Tree tree = new KD_Tree(Math.abs(temp[0]));

        for(int i = 1; i < temp.length; i++){
            tree.insert(temp[i]);
        }

        System.out.println("original tree");
        tree.print_tree(tree.root);

        distance_query e = new distance_query();

        ArrayList<Integer> result = e.dis_query(2,2,temp);
        System.out.println("Answer for Question3");
        System.out.println(result.toString());


    }
}    