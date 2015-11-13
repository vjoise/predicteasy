package com.predicteasy.utils;

/**
 * @author Venkat & Gaurav (KDDM project)
 */
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
	
	public static Double average(Double... reviews){
		Double total = new Double(0);
		for(Double review : reviews)
			total+= review;
		return total/reviews.length;
	}
	
	public static void printMem(){
		System.out.println("*********************");
		System.out.println("Memory stats:");
		System.out.println("Total (MB) : " + Runtime.getRuntime().totalMemory()/(1024*1024));
		System.out.println("Free (MB) : " + Runtime.getRuntime().freeMemory()/(1024*1024));
		System.out.println("Used (MB) : " + (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory())/(1024*1024));
		System.out.println("*********************");
	}
}
