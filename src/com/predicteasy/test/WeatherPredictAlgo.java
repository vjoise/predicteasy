package com.predicteasy.test;

import java.util.Map;

import com.predicteasy.datasource.CSVDataSource;
import com.predicteasy.datasource.DataSource;
import com.predicteasy.datastore.IndexedDataStore;
import com.predicteasy.dto.Node;
import com.predicteasy.model.DecisionTreePredictor;

public class WeatherPredictAlgo {

	public static void main(String[] args) throws Exception {
		/* Initiate Data Fetch from data.csv */
        DataSource csvSource = new CSVDataSource("WeatherData_Training.csv");
        Map<Long, Node> inputData = csvSource.getData();
        
        //--> TODO : Assume : have all the KNNs
//        Map<Node, List<Node>> neighborsMap = new HashMap<Node, List<Node>>();
//        neighborsMap.put();
        
        /* Data source that will have this data initialized in all indexes for fast query*/
        IndexedDataStore dataStore = new IndexedDataStore(inputData);
        
		/* Initiate rating predictor here. */
        DecisionTreePredictor predictor = new DecisionTreePredictor(dataStore);
	}

}
