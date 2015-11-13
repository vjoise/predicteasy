package com.predicteasy.test;

import com.predicteasy.datasource.CSVDataSource;
import com.predicteasy.datasource.DataSource;
import com.predicteasy.datastore.DataStore;
import com.predicteasy.dto.ProductKey;
import com.predicteasy.knn.NearestNeighborFinder;
import com.predicteasy.model.BasePredictor;
import com.predicteasy.utils.Utils;

/**
 * KDDM term project
 * 
 * @author Venkat & Gaurav (KDDM project)
 */
public class PredictionTestRunner {

	public static boolean IS_DEBUG_MODE = false;
	public static final String DATA_SOURCE_FILE = "beer_reviews.csv";
	
	private static final ProductKey PREDICT_QUERY = new ProductKey("English Strong Ale", "stcules");
	
    private BasePredictor predictor;
    private NearestNeighborFinder nearestNeighborFinder;

    public PredictionTestRunner(String dataSourceFile, boolean hasHeader) throws Exception{
    	Utils.printMem();
    	
        /* Initiate Data Fetch from data.csv */
    	System.out.println("Loading data from source file : " + dataSourceFile);
        DataSource csvSource = new CSVDataSource(dataSourceFile, hasHeader);
        Utils.printMem();
        
        /** load the data store */
        DataStore dataStore = csvSource.getData();
        System.out.println("DataStore loaded with entries : " + dataStore.size());
        Utils.printMem();
        
        //Find the mean average rating considering all beers and all users
        Double meanBeerRating = dataStore.getMeanProductRating();
        System.out.println("Mean Beer rating (all users): " + meanBeerRating);
        Utils.printMem();
        
        //Find the average rating of beer in query (for all users except prediction user)
        Double averageRatingOfQueryBeer = dataStore.getAverageProductRating(PREDICT_QUERY);
        System.out.println("Average rating of Query Beer [" + PREDICT_QUERY.getProductId() + "] is : " + averageRatingOfQueryBeer);
        Utils.printMem();
        
        //Find the average rating of all beers as done by user in prediction query
        Double averageRatingByQueryUser = dataStore.getAverageUserRating(PREDICT_QUERY);
        System.out.println("Average rating of Query User [" + PREDICT_QUERY.getReviewer() + "] is : " + averageRatingByQueryUser);
        Utils.printMem();
        
        //Global baseline using offset from product average and user average 
        Double productAvgOffset = Math.abs(averageRatingOfQueryBeer - meanBeerRating);
        Double userAvgOffset = Math.abs(averageRatingByQueryUser - meanBeerRating);
        
        Double globalBaseLine = meanBeerRating
        		+ ((averageRatingOfQueryBeer > meanBeerRating) ? productAvgOffset : -1 * productAvgOffset)
        		+ ((averageRatingByQueryUser > meanBeerRating) ? userAvgOffset : -1 * userAvgOffset);
        System.out.println("Global baseline estimate for Prediction Query [Beer: "+ PREDICT_QUERY.getProductId() + ", Reviewer: " + PREDICT_QUERY.getReviewer() + "] is : " + globalBaseLine);
        Utils.printMem();
        
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
