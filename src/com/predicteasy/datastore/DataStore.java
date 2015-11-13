package com.predicteasy.datastore;

import java.util.List;
import java.util.Map;

import com.predicteasy.dto.ProductKey;
import com.predicteasy.dto.ProductReviewDetails;

/**
 * @author Venkat & Gaurav (KDDM project)
 */
public interface DataStore {
	public void addData(String[] values);
	public long size();

	public Double getMeanProductRating();
	public Double getAverageProductRating(ProductKey predictQuery);
	public Double getAverageUserRating(ProductKey predictQuery);
	
	public Map<ProductKey, Number> getReviewSummary(ProductKey productKey);
	public List<ProductReviewDetails> getProductReviews(ProductKey productKey);
}
