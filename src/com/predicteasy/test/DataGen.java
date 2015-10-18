package com.predicteasy.test;

import java.io.File;
import java.io.FileWriter;
import java.util.Random;

/**
 * Created by A0120096(Venkatesh) on 27/9/2015.
 */
public class DataGen {

    public static void main(String[] a) throws Exception{

        File file = new File("c:/nus/sample.csv");

        StringBuilder builder = new StringBuilder();
        for(int i=0;i<1000;i++){
            builder.append(i%100);
            builder.append(",");
            Random random = new Random();
            builder.append((random.nextFloat() % 100.0f) * 100 + "," );    //alcohol content
            builder.append(random.nextInt(6) + ",");   //style
            builder.append(random.nextInt(6) + "," );   //look
            builder.append(random.nextInt(6) + "\n");   //overall rating
        }
        //System.out.println(builder.toString());
        FileWriter fileWriter = new FileWriter(file);
        fileWriter.write(builder.toString());
    }
}
