package com.predicteasy.test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.predicteasy.data.CSVDataSource;
import com.predicteasy.data.DataSource;
import com.predicteasy.knn.EuclideanNearestNeighborFinder;
import com.predicteasy.knn.NearestNeighborFinder;
import com.predicteasy.knn.Node;
import com.predicteasy.model.BasePredictor;
import com.predicteasy.model.PredictionClass;
import com.predicteasy.model.RatingPredictor;

public class PredictionTestRunner {

    private BasePredictor predictor;

    private NearestNeighborFinder nearestNeighborFinder;

    private CSVDataSource dataFetcher;

    public PredictionTestRunner() throws Exception{

        /* Initiate Data Fetch from data.csv */
        DataSource csvSource = new CSVDataSource("data.csv");
        Map<Long, Node> inputData = csvSource.getData();

        /* The value of K will be usually Math.sqrt(rowCount) */
        int valueOfK = dataFetcher.getValueOfK();

        /* Initiate the KNN Finder with the k-factor and the input data. */
        nearestNeighborFinder = new EuclideanNearestNeighborFinder(valueOfK, inputData);

        /* Feed initial data to KNN Engine along with test data. */
        List<Node> queryNodes = dataFetcher.getQueryNodes();

        /* Map to hold neighboring nodes for a given "query" Node.*/
        Map<Node, List<Node>> neighborsMap = new HashMap<Node, List<Node>>();
        for(Node node : queryNodes){
            neighborsMap.put(node, nearestNeighborFinder.findNearestNeighbors(node));
        }

        /* Initiate rating predictor here. */
        predictor = new RatingPredictor(neighborsMap);

        /* Predict the value for the input query Q, along with the generated KNNs in the previous step. */
        for(Node node : queryNodes){
            PredictionClass predictionClass = predictor.predictForQuery(node);

        }
    }

    public static void main(String[] args) throws Exception {
	  new PredictionTestRunner();
    }
}
