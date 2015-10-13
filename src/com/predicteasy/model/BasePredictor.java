package com.predicteasy.model;

import com.predicteasy.knn.Node;

import java.util.List;
import java.util.Map;

/**
 * Created by A0120096(Venkatesh) on 13/10/2015.
 */
public interface BasePredictor {

    public PredictionClass predictForQuery(Node node);
}
