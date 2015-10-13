package com.predicteasy.knn;

import java.util.List;
import java.util.Map;

import com.predicteasy.dto.Node;

/**
 * Created by A0120096(Venkatesh) on 13/10/2015.
 */
public class EuclideanNearestNeighborFinder implements NearestNeighborFinder {

    private int valueOfK;

    public EuclideanNearestNeighborFinder(int valueOfK, Map<Long, Node> inputData) {
        this.valueOfK = valueOfK;
    }

    @Override
    public List<Node> findNearestNeighbors(Node queryNode) {
        return null;
    }
}
