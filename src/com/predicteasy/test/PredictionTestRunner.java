package com.predicteasy.test;

import org.apache.commons.lang3.StringUtils;

import com.predicteasy.datasource.CSVDataSource;
import com.predicteasy.datasource.DataSource;
import com.predicteasy.datastore.DataStore;
import com.predicteasy.knn.NearestNeighborFinder;
import com.predicteasy.model.BasePredictor;

public class PredictionTestRunner {

	public static boolean IS_DEBUG_MODE = true;
	public static final String DATA_SOURCE_FILE = "/Users/gaurav/Downloads/KDDM/predicteasy/resources/beer_reviews.csv";
	
    private BasePredictor predictor;

    private NearestNeighborFinder nearestNeighborFinder;

    private CSVDataSource dataSource;

    public PredictionTestRunner(String dataSourceFile, boolean hasHeader) throws Exception{
    	
        /* Initiate Data Fetch from data.csv */
    	System.out.println("Loading data from source file : " + dataSourceFile);
        DataSource csvSource = new CSVDataSource(dataSourceFile, hasHeader);
        
        /** load the data store */
        DataStore dataStore = csvSource.getData();
        System.out.println("DataStore loaded with entries : " + dataStore.size());
        
        //Find the average rating for each user per beer
        Double meanAvgRating = dataStore.getMeanProductRating();
        System.out.println("Mean average OverallRating : " + meanAvgRating);
        
        //Task 2 : Find the average rating for beer + customer in query
        
        //Task 3 : Calculate the global baseline
        
        //Task 4 : Find the distance or similarity of beers with the beer from query
        
        //Prediction using the knn neighbours and using average baseline
        
//        /* The value of K will be usually Math.sqrt(rowCount) */
//       int valueOfK = dataSource.getValueOfK();
//
//        /* Initiate the KNN Finder with the k-factor and the input data. */
//        nearestNeighborFinder = new EuclideanNearestNeighborFinder(valueOfK, inputData);
//
//        /* Feed initial data to KNN Engine along with test data. */
//        List<Node> queryNodes = dataSource.getQueryNodes();
//
//        /* Map to hold neighboring nodes for a given "query" Node.*/
//        Map<Node, List<Node>> neighborsMap = new HashMap<Node, List<Node>>();
//        for(Node node : queryNodes){
//            neighborsMap.put(node, nearestNeighborFinder.findNearestNeighbors(node));
//        }
//
//        /* Initiate rating predictor here. */
//        predictor = new RatingPredictor(neighborsMap);
//
//        /* Predict the value for the input query Q, along with the generated KNNs in the previous step. */
//        for(Node node : queryNodes){
//            PredictionClass predictionClass = predictor.predictForQuery(node);
//
//        }
    }

    public static void main(String[] args) throws Exception {
	  new PredictionTestRunner(DATA_SOURCE_FILE, true);
    }
}
