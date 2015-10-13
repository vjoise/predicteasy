package com.predicteasy.knn;

import java.util.List;

/**
 * Created by A0120096(Venkatesh) on 13/10/2015.
 */
public interface NearestNeighborFinder {

    public List<Node> findNearestNeighbors(Node queryNode);

}
