package com.predicteasy.dto;

import com.predicteasy.utils.Utils;

public class ProductReviewDetails {
	private Number overallReview;
	private Number aromaReview;
	private Number appearanceReview;
	
	public ProductReviewDetails(Number overallReview, Number aromaReview,
			Number appearanceReview) {
		super();
		this.overallReview = overallReview;
		this.aromaReview = aromaReview;
		this.appearanceReview = appearanceReview;
	}

	public static ProductReviewDetails mergeReviews(ProductReviewDetails review1, ProductReviewDetails review2){
		return new ProductReviewDetails(Utils.average((Double)review1.overallReview, (Double)review1.overallReview),
				Utils.average((Double)review1.aromaReview, (Double)review1.aromaReview),
				Utils.average((Double)review1.appearanceReview, (Double)review1.appearanceReview));
				
	}
}
