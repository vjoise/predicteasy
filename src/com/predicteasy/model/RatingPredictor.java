package com.predicteasy.model;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.predicteasy.dto.Node;

/**
 * A generic rating predictor based on customer id and product attributes.
 * Created by A0120096(Venkatesh) on 13/10/2015.
 */
public class RatingPredictor implements BasePredictor {

    private Map<Node, List<Node>> neighborsMap = new HashMap<Node, List<Node>>();

    public RatingPredictor(Map<Node, List<Node>> neighborsMap) {
        this.neighborsMap = neighborsMap;
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
