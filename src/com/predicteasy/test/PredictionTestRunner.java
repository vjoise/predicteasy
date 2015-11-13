package com.predicteasy.test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.predicteasy.datasource.CSVDataSource;
import com.predicteasy.datasource.DataSource;
import com.predicteasy.datastore.DataStore;
import com.predicteasy.dto.Node;
import com.predicteasy.knn.EuclideanNearestNeighborFinder;
import com.predicteasy.knn.NearestNeighborFinder;
import com.predicteasy.model.BasePredictor;
import com.predicteasy.model.PredictionClass;
import com.predicteasy.model.RatingPredictor;

public class PredictionTestRunner {

	public static final String DATA_SOURCE_FILE = "/Users/gaurav/Downloads/KDDM/predicteasy/resources/beer_reviews.csv";
	
    private BasePredictor predictor;

    private NearestNeighborFinder nearestNeighborFinder;

    private CSVDataSource dataSource;

    public PredictionTestRunner(String dataSourceFile, boolean hasHeader) throws Exception{

        /* Initiate Data Fetch from data.csv */
        DataSource csvSource = new CSVDataSource(dataSourceFile, hasHeader);
        DataStore inputData = csvSource.getData();

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
