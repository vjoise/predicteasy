#This is a converter from input data to a review matrix
#Columns -> Beers
#Rows    -> Customers
import csv
import math
import operator

FEATURE_SET = ['review_overall', 'review_aroma', 'review_palate', 'review_taste']
REVIEW_OVERALL = 3 #review_overall
CUSTOMER_ID = 6 #review_profilename

valueOfK = 10 #Top 10 customers for testing purpose.

#Compute euclidean distance.
def computeDistance(testData, data) :
    distance = 0
    leftValue = float(testData)
    rightValue = float(data)
    distance = pow((leftValue- rightValue), 2)
    return math.sqrt(distance)

#This finds the nearest customer by checking his review.
def findSimilarCustomers(customerId, availableCustomerRows, availableBeerColumns):

    #The beers reviewed by this test customer
    ratingsByTestCustomer = availableCustomerRows.get(customerId)

    listOfReviews = []
    #Find common beers reviewed
    #For all the beers
    dist = []
    returnList = []
    for rating in ratingsByTestCustomer :
        beers = availableBeerColumns.get(rating.product)
        for review in beers:
            if customerId == review[CUSTOMER_ID] :
                continue
            #print review
            #Compute distance of reviews with the test customer's data one-by-one.
            distance = computeDistance(rating.overallRating, review[REVIEW_OVERALL])
            row = [customerId, review[CUSTOMER_ID]] + [distance]
            dist.append(row)
            #Return the best possible match by sorting the list with min distance.
    dist.sort(key=operator.itemgetter(2))
    for i in range(1,10) :
        returnList.append(dist[i][1])
    
    return returnList
