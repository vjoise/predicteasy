
CUSTOMER_ID = 6 #review_profilename
BEER_NAME = 10 #beer_name
REVIEW_OVERALL = 3 #review_overall
COMMON_REVIEWERS_MAP_KEY = 6

#This is a class to compute global + collaborative values.
class PredictionModel :

    testCustomer = ''
    similarCustomers = []
    similarBeers = []
    availableBeerColumns = {}
    availableCustomerRows = {}
    baselineEstimate = 0
    
    def __init__ (self, testCustomer, similarCustomers, similarBeers, availableBeerColumns, availableCustomerRows):
        self.testCustomer = testCustomer
        self.similarCustomers = similarCustomers
        print "Similar beers", similarBeers
        self.similarBeers = similarBeers
        self.availableBeerColumns = availableBeerColumns
        self.availableCustomerRows = availableCustomerRows
        
    inputData=[]
    
    def computeGlobalBaseline(self, productName):
        #Mean rating across all beers
        #print "Overall Rating : ", MEAN_PRODUCT_RATING
        print "# of reviews for :", productName ,' is : ',len(self.availableBeerColumns.get(productName))
        tempSum = 0

        for dat in self.availableBeerColumns[productName] :
            tempSum += round(float(dat[REVIEW_OVERALL]), 1)
        meanRatingForProduct = round(tempSum / len(self.availableBeerColumns.get(productName)), 1)
        print "Mean rating for product : ", productName, " is :: ", meanRatingForProduct

        #Find the mean rating for this customer
        tempSum = 0
        ratingsForThisUser = self.availableCustomerRows[self.testCustomer]
        print "#ratings for user : ", self.testCustomer, ' is ',  len(ratingsForThisUser)
        for rating in ratingsForThisUser :
            tempSum += round(float(rating.overallRating), 10)
           # print rating.product, rating.overallRating, '\n' 
        #meanUserRating = round(tempSum / len(ratingsForThisUser), 1)
        print "Temp sum", tempSum
        print "rating count", len(ratingsForThisUser)
        meanUserRating = float(tempSum / len(ratingsForThisUser))
        print "Mean rating of user***  : ", self.testCustomer, " is :: ", meanUserRating
        
        #Compared to other users, this user rates it higher/lower
        differenceInRating = meanRatingForProduct - meanUserRating

        #This is the baseline estimate
        baselineEstimate = meanRatingForProduct + differenceInRating

        return baselineEstimate
        
    def computeFilteredRatingEstimate(self, productName):
        #Within this set of beers find the first most similar one ( with minimum distance ).
        sum = 0
        avg = {}
        #Now get all the ratings for similar customers for these beers and take an average.
        for beer in self.similarBeers:
            totalCount = 0
            sumOfRatings = 0
            for record in self.availableBeerColumns[beer] :
            	#Choose only those customers who are similar for collaborative filtering.
                if record[CUSTOMER_ID] in self.similarCustomers :
                    sumOfRatings += float(record[REVIEW_OVERALL])
                    totalCount += 1
            if totalCount != 0 :
                avg[beer] = float(sumOfRatings / totalCount)
        return avg
