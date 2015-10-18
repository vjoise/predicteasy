package com.predicteasy.utils;

public class Utils {

	/**
     * Entropy (p,q) = -p log2 (p) - q log2 (q)
     * @param p --> generally denoting totalPositives or anyone class
     * @param q --> generally denoting totalNegatives or any one class
     * @return
     */
	public static double entropy(double p, double q){
    	return -(p * Utils.log(p, 2)) - (q * Utils.log(q, 2));
    }
	
	public static double log(double x, int base){
	    return (Math.log(x) / Math.log(base));
	}
}
