package com.predicteasy.datastore;

import java.util.Map;

import com.predicteasy.dto.Node;

public class IndexedDataStore implements DataStore{

	private long positiveTargets;
	private long negativeTargets;
	
	public IndexedDataStore(Map<Long, Node> data){
		//TODO
	}
	
	public long getTotalPositives(){
		return positiveTargets;
	}
	
	public long getTotalNegatives(){
		return negativeTargets;
	}
}
