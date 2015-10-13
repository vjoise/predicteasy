package com.predicteasy.datasource;

import java.util.Map;

import com.predicteasy.dto.Node;

public interface DataSource {

	public Map<Long, Node> getData();
}
