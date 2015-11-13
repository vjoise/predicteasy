package com.predicteasy.datasource;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.apache.commons.lang3.StringUtils;

import com.predicteasy.datastore.DataStore;
import com.predicteasy.datastore.IndexedProductDataStore;
import com.predicteasy.dto.Node;
import com.predicteasy.test.PredictionTestRunner;
import com.predicteasy.utils.Utils;

/**
 * A simple implementation to fetch csv data into a map.
 *
 * @author Venkat & Gaurav (KDDM project)
 */
public class CSVDataSource implements DataSource{

    private static final String SEPARATOR = ",";
    
    private DataStore dataStore = null;
    private List<Node> queryNodes;
    private int valueOfK;
    
    public CSVDataSource(String csvFileName, boolean hasHeader) throws Exception{
    	System.out.println("Reading data from csv file : " + csvFileName);
    	Utils.printMem();  	
    	this.dataStore = this.loadFile(new File(csvFileName), hasHeader);
    }

    private DataStore loadFile(File inputFile, boolean hasHeader) throws Exception{
    	DataStore dataStore = null;
    	Map<Long, Node> data = new HashMap<Long, Node>();
    	Scanner scanner = new Scanner(inputFile);
    	
    	try{
    		//Pick header and initialize the index store
    		if(hasHeader){
				String header = scanner.nextLine();
				System.out.println("Header : " + header);
				dataStore = new IndexedProductDataStore(header.split(SEPARATOR));
    		}
    		
    		long rowNumber = 0;
    		while(scanner.hasNext()){
    			String[] values =  scanner.nextLine().split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)", -1);

    			if(PredictionTestRunner.IS_DEBUG_MODE) 
    				System.out.println("Read line : " + Arrays.toString(values));
    			
    			dataStore.addData(values);
//    			int columnNumber = 0;
    			//for(String col : columns){
//    				Node node = new Node();
    				//node.addAttribute(COLUMN_HEADER_MAP.get(columnNumber), Integer.parseInt(col));
    				//data.put(rowNumber++, node);
    				//columnNumber ++;
    			//}
    			
    			if(PredictionTestRunner.IS_DEBUG_MODE) 
    				System.out.println("Row count : "+ rowNumber++);
    		}
    	}finally{
    		if(PredictionTestRunner.IS_DEBUG_MODE) {
    			System.out.println("Finished reading all csv data");
    			System.out.println("Read data of size :" + dataStore.size());
    		}
    		scanner.close();
    		Runtime.getRuntime().gc();
    		Utils.printMem();
    	}
    	valueOfK = (int)Math.sqrt(dataStore.size());
    	
    	return dataStore;
    }

	@Override
	public DataStore getData() {
		return dataStore;
	}
	
    public int getValueOfK() {
        return valueOfK;
    }

    //TODO
    public List<Node> getQueryNodes() {
        return queryNodes;
    }
}

