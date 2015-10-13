package com.predicteasy.dto;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Node which represents data.
 * Created by A0120096(Venkatesh) on 13/10/2015.
 */
public class Node {

   private Map<String, Number> attributesMap = new HashMap<String, Number>();

   private List<Node> neighbors;

   private boolean isLeaf;
   
   public void addToNNList(Node node){
        this.neighbors.add(node);
   }

   public List<Node> getNNList(){
       return this.neighbors;
   }

   public void addAttribute(String key, Number value){
       attributesMap.put(key, value);
   }

    public Number getAttribute(String key){
        return attributesMap.get(key);
    }
    
    public boolean isLeafNode(){
    	return isLeaf;
    }

}
