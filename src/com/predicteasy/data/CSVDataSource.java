package com.predicteasy.data;

import java.io.File;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import com.predicteasy.knn.Node;

/**
 * A simple implementation to fetch csv data into a map.
 *
 * Created by A0120096(Venkatesh) on 13/10/2015.
 */
public class CSVDataSource implements DataSource{

    private static Map<Integer, String> COLUMN_HEADER_MAP = new HashMap<Integer, String>();

    /*We can change this dataset anytime.*/
    static{
        COLUMN_HEADER_MAP.put(1, "CUSTOMERID");
        COLUMN_HEADER_MAP.put(2, "BREWERID");
        COLUMN_HEADER_MAP.put(3, "ALCOHOLCONTENT");
        COLUMN_HEADER_MAP.put(4, "CATEGORY");
        COLUMN_HEADER_MAP.put(5, "RATING");
    }

    private Map<Long, Node> dataMap = Collections.emptyMap();
    private List<Node> queryNodes;
    private int valueOfK;
    
    public CSVDataSource(String csvFileName) throws Exception{
    	System.out.println("Reading data from csv file : " + csvFileName);
    	this.dataMap = this.loadFile(new File(csvFileName));
    }

    private Map<Long, Node> loadFile(File inputFile) throws Exception{
    	Map<Long, Node> data = new HashMap<Long, Node>();
    	Scanner scanner = new Scanner(inputFile);
    	try{
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
    	}finally{
    		System.out.println("Finished reading all csv data");
    		scanner.close();
    	}
    	System.out.println("Read data of size :" + data.size());
    	valueOfK = (int)Math.sqrt(dataMap.size());
    	return data;
    }

	@Override
	public Map<Long, Node> getData() {
		return dataMap;
	}
	
    public int getValueOfK() {
        return valueOfK;
    }

    //TODO
    public List<Node> getQueryNodes() {
        return queryNodes;
    }
}

