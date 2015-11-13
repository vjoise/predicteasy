package com.predicteasy.datastore;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.locks.ReentrantLock;

import org.apache.commons.lang3.StringUtils;

import com.predicteasy.dto.ProductKey;
import com.predicteasy.dto.ProductReviewDetails;
import com.predicteasy.test.PredictionTestRunner;

/**
 * Builds various indexes of product ratings as per model requirements
 * @author Venkat & Gaurav (KDDM project)
 */
public class IndexedProductDataStore implements DataStore{

	private static List<String> KEY_COLUMNS = new ArrayList<String>();
	private static List<String> REVIEW_COLUMNS = new ArrayList<String>();

	//This can be changed, order is important
	static{
		//brewery_id,brewery_name,review_time,review_overall,review_aroma,review_appearance,review_profilename,
		//beer_style,review_palate,review_taste,beer_name,beer_abv,beer_beerid
		KEY_COLUMNS.add("beer_name");KEY_COLUMNS.add("review_profilename");
		REVIEW_COLUMNS.add("review_overall"); REVIEW_COLUMNS.add("review_aroma"); REVIEW_COLUMNS.add("review_appearance");
	}	
	private Map<String, Integer> KEY_COLUMN_INDEX_MAP = new HashMap<String, Integer>();
	private Map<String, Integer> REVIEW_COLUMN_INDEX_MAP = new HashMap<String, Integer>();

	private String[] header;
	private ReentrantLock lock = new ReentrantLock();
	private Map<ProductKey, ProductReviewDetails> reviewData = new HashMap<ProductKey, ProductReviewDetails>();

	public IndexedProductDataStore(String[] header){
		this.header = header;

		//build indexes, which will be used when adding data
		for(int index = 0; index < header.length; index++){
			String headerField = header[index];
			if(KEY_COLUMNS.contains(headerField)){
				KEY_COLUMN_INDEX_MAP.put(headerField, index);
			}
			if(REVIEW_COLUMNS.contains(headerField)){
				REVIEW_COLUMN_INDEX_MAP.put(headerField, index);
			}
		}
	}

	public void addData(String[] values){
		try{
			lock.lock();
			if(!isValidInput(values)){
				if(PredictionTestRunner.IS_DEBUG_MODE)
					System.out.println("Invalid input, ignore values : " + Arrays.toString(values));
				return;
			}

			ProductKey key = new ProductKey(values[KEY_COLUMN_INDEX_MAP.get(KEY_COLUMNS.get(0))], values[KEY_COLUMN_INDEX_MAP.get(KEY_COLUMNS.get(1))]);

			ProductReviewDetails review = new ProductReviewDetails(Double.parseDouble(values[REVIEW_COLUMN_INDEX_MAP.get(REVIEW_COLUMNS.get(0))]), 
					Double.parseDouble(values[REVIEW_COLUMN_INDEX_MAP.get(REVIEW_COLUMNS.get(1))]), 
					Double.parseDouble(values[REVIEW_COLUMN_INDEX_MAP.get(REVIEW_COLUMNS.get(2))]),
					Long.parseLong(values[2])
					);

			//merge to any existing review for same key
			if(reviewData.containsKey(key)){
				ProductReviewDetails existing = reviewData.get(key);
				//merge the existing with this review
				ProductReviewDetails mergedReview = ProductReviewDetails.mergeReviews(existing, review);
				review = mergedReview;
			}

			reviewData.put(key, review);
		}finally{
			lock.unlock();
		}
	}

	private boolean isValidInput(String[] values){
		for(int index : KEY_COLUMN_INDEX_MAP.values()){
			if(index > values.length || StringUtils.isEmpty(values[index])){
				return false;
			}
		}
		for(int index : REVIEW_COLUMN_INDEX_MAP.values()){
			if(index > values.length  || StringUtils.isEmpty(values[index])){
				return false;
			}
		}
		return true;
	}

	@Override
	public long size() {
		try{
			lock.lock();
			return reviewData.size();
		}finally{
			lock.unlock();
		}
	}		

	/**
	 * average rating (considering overall only) for all products for all users
	 */
	@Override
	public Double getMeanProductRating() {
		try{
			lock.lock();
			
			Double overallRating = new Double(0);
			for(Entry<ProductKey, ProductReviewDetails> entry : reviewData.entrySet()){
				overallRating += (Double)entry.getValue().getOverallReview();
			}
			return overallRating/reviewData.entrySet().size();
		}finally{
			lock.unlock();
		}
	}

	/**
	 * Return average product review summary by a 
	 * @param productKey
	 * @return
	 */
	@Override
	public Map<ProductKey, Number> getReviewSummary(ProductKey productKey) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public List<ProductReviewDetails> getProductReviews(ProductKey productKey) {
		// TODO Auto-generated method stub
		return null;
	}

	/** 
	 * Average product rating for this beer by all users (except the query user)
	 * (Though review for this beer by query customer shouldnt be present, still checking to avoid problem with test data)
	 */
	@Override
	public Double getAverageProductRating(ProductKey predictQuery) {
		String queryBeer = predictQuery.getProductId();
		String queryUser = predictQuery.getReviewer();
		
		//Find all entries for this beer (excluding the query user)
		try{
			lock.lock();
			Double overallQueryProductRating = new Double(0);
			Double counter = new Double(0);
			
			for(Entry<ProductKey, ProductReviewDetails> entry : reviewData.entrySet()){
				if(StringUtils.equals(queryBeer, entry.getKey().getProductId()) 
						&& !StringUtils.equals(queryUser, entry.getKey().getReviewer())) {
					
					overallQueryProductRating += (Double)entry.getValue().getOverallReview();
					counter++;
				}
			}
			
			return overallQueryProductRating/counter;
		}finally{
			lock.unlock();
		}
	}

	/** 
	 * Average rating for all beers by query user 
	 * (except the query beer itself - though query beer review for this user will not be in data, still checking to avoid mistakes with test data)
	*/
	@Override
	public Double getAverageUserRating(ProductKey predictQuery) {
		String queryBeer = predictQuery.getProductId();
		String queryUser = predictQuery.getReviewer();
		
		//Find all entries for this user (excluding the query beer)
		try{
			lock.lock();
			Double overallQueryUserRating = new Double(0);
			Double counter = new Double(0);
			
			for(Entry<ProductKey, ProductReviewDetails> entry : reviewData.entrySet()){
				if(!StringUtils.equals(queryBeer, entry.getKey().getProductId()) 
						&& StringUtils.equals(queryUser, entry.getKey().getReviewer())) {
					
					overallQueryUserRating += (Double)entry.getValue().getOverallReview();
					counter++;
				}
			}
			
			return overallQueryUserRating/counter;
		}finally{
			lock.unlock();
		}
	}
}
