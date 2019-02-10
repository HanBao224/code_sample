package com.company;
import org.junit.Test;
import org.jboss.arquillian.container.test.api.Deployment;
import org.jboss.arquillian.junit.Arquillian;
import org.jboss.shrinkwrap.api.ShrinkWrap;
import org.jboss.shrinkwrap.api.asset.EmptyAsset;
import org.jboss.shrinkwrap.api.spec.JavaArchive;
import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;


public class KD_TreeTest {
    @Test

    public void main() throws Exception{
        int[] case1 = new int[]{2,1,3};
        KD_Tree tree = new KD_Tree(case1[0]);
        //assertEquals(new int[]{1,2,3},);

    }




}

