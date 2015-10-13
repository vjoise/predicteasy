package com.predicteasy.data;

import java.util.Map;

import com.predicteasy.knn.Node;

public interface DataSource {

	public Map<Long, Node> getData();
}
