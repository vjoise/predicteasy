package com.predicteasy.dto;

/**
 * For more than one review for same product by same user, we merge and take average
 * 
 * @author Venkat & Gaurav (KDDM project)
 *
 */
public class ProductKey {
	private String productId;
	private String reviewer;

	public ProductKey(String beerName, String reviewer) {
		super();
		this.productId = beerName;
		this.reviewer = reviewer;
	}
	
	public String getProductId() {
		return productId;
	}

	public String getReviewer() {
		return reviewer;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result
				+ ((productId == null) ? 0 : productId.hashCode());
		result = prime * result
				+ ((reviewer == null) ? 0 : reviewer.hashCode());
		return result;
	}
	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		ProductKey other = (ProductKey) obj;
		if (productId == null) {
			if (other.productId != null)
				return false;
		} else if (!productId.equals(other.productId))
			return false;
		if (reviewer == null) {
			if (other.reviewer != null)
				return false;
		} else if (!reviewer.equals(other.reviewer))
			return false;
		return true;
	}
	
	
}
