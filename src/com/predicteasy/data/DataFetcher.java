package com.predicteasy.data;

import com.predicteasy.knn.Node;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

/**
 * A simple implementation to fetch csv data into a map.
 *
 * Created by A0120096(Venkatesh) on 13/10/2015.
 */
public class DataFetcher {

    private File inputFile;

    private static Map<Integer, String> COLUMN_HEADER_MAP = new HashMap<Integer, String>();

    /*We can change this dataset anytime.*/
    static{
        COLUMN_HEADER_MAP.put(1, "CUSTOMERID");
        COLUMN_HEADER_MAP.put(2, "BREWERID");
        COLUMN_HEADER_MAP.put(3, "ALCOHOLCONTENT");
        COLUMN_HEADER_MAP.put(4, "CATEGORY");
        COLUMN_HEADER_MAP.put(5, "RATING");
    }

    private int valueOfK;

    private static final Map<Long, Node> INPUT_DATA = new HashMap<Long, Node>();

    private List<Node> queryNodes;

    public Map<Long, Node> getData(File inputFile) throws Exception{
        this.inputFile = inputFile;
        Map<Long, Node> data = new HashMap<Long, Node>();
        Scanner scanner = new Scanner(inputFile);
        long rowNumber = 0;
        while(scanner.hasNext()){
            String columns[] = scanner.nextLine().split(",");
            int columnNumber = 0;
            for(String col : columns){
                Node node = new Node();
                node.addAttribute(COLUMN_HEADER_MAP.get(columnNumber), Integer.parseInt(col));
                data.put(rowNumber++, node);
                columnNumber ++;
            }
        }
        return data;
    }

    public int getValueOfK() {
        return (int)Math.sqrt(INPUT_DATA.size());
    }

    public List<Node> getQueryNodes() {
        return queryNodes;
    }
}

