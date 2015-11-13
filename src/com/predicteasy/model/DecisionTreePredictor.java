package com.predicteasy.model;

import com.predicteasy.datastore.DataStore;
import com.predicteasy.dto.Node;
import com.predicteasy.utils.Utils;

/**
 * Decision tree based prediction model
 */
public class DecisionTreePredictor implements BasePredictor {

	private boolean isDebug = Boolean.parseBoolean(System.getProperty("debug.mode", "false"));
	
	private DataStore dataSource;
    
    public DecisionTreePredictor(DataStore dataStore) {
        dataSource = dataStore;
        this.initialize();
    }

    /*
     * Build decision tree
     * Algorithm documentation : http://www.saedsayad.com/decision_tree.htm
     */
    private void initialize() {
    	System.out.println("Building decision tree");
        //Step 1 : Pick the root node and calculate target entropy i.e for all result class.
    	//e.g. if the result or KNN or training set has x positive and y negatives, then calc its entropy
    	double totalPos = dataSource.getTotalPositives();
    	double totalNeg = dataSource.getTotalNegatives();
    	
    	double targetEntropy = Utils.entropy(totalPos, totalNeg);
    	System.out.println("Target entropy is : " + targetEntropy);
    	
    	//TODO : Need to check if 
    	//Step 2 : Find entropy for each attribute and info gain.
    	//Based on max gain, pick the attribute to start building tree.
    	
    	//Step 3 : Repeat the above till all data is parsed
    }
    
    
    //TODO
    private double calcInfoGain(){
    	return 0d;
    }
    
    @Override
    public PredictionClass predictForQuery(Node node) {

        /*Start with UNKNOWN class*/
        PredictionClass predictionClass = PredictionClass.UNKNOWN;

        /* For all the similar items, get the key. 
         * We need to score the customer based on his previous rating for a similar kind of beer.
         **/
        for(Node nearestNode : node.getNNList()){
            nearestNode.getAttribute("");
        }

        return predictionClass;
    }
}
