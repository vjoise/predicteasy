package com.predicteasy.knn;

import java.util.List;

import com.predicteasy.dto.Node;

/**
 * @author Venkat & Gaurav (KDDM project)
 */
public interface NearestNeighborFinder {

    public List<Node> findNearestNeighbors(Node queryNode);

}
