#This is a converter from input data to a review matrix
#Columns -> Beers
#Rows    -> Customers
from csv_loader import *
import math
import operator
import knn_beer as kv
import knn_customer as knnc
from timeit import default_timer


#This is a class to compute global + collaborative values.
class PredictionModel :

    testCustomer = ''
    similarCustomers = []
    similarBeers = []
    baselineEstimate = 0
    
    def __init__ (self, testCustomer, similarCustomers, similarBeers):
        self.testCustomer = testCustomer
        self.similarCustomers = similarCustomers
        self.similarBeers = similarBeers
        
    inputData=[]
    
    def computeGlobalBaseline(self, productName):
        #Mean rating across all beers
        #print "Overall Rating : ", MEAN_PRODUCT_RATING
        print "# of reviews for :", productName ,' is : ',len(availableBeerColumns.get(productName))
        tempSum = 0

        for dat in availableBeerColumns[productName] :
            tempSum += round(float(dat[REVIEW_OVERALL]), 1)
        meanRatingForProduct = round(tempSum / len(availableBeerColumns.get(productName)), 1)
        print "Mean rating for product : ", productName, " is :: ", meanRatingForProduct

        #Find the mean rating for this customer
        tempSum = 0
        ratingsForThisUser = availableCustomerRows[self.testCustomer]
        print "#ratings for user : ", self.testCustomer, ' is ',  len(ratingsForThisUser)
        for rating in ratingsForThisUser :
            tempSum += round(float(rating.overallRating), 1)
           # print rating.product, rating.overallRating, '\n' 
        meanUserRating = round(tempSum / len(ratingsForThisUser), 1)
        print "Mean rating of user : ", self.testCustomer, " is :: ", meanUserRating
        
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
        for beer in similarBeers:
            totalCount = 0
            sumOfRatings = 0
            for record in availableBeerColumns[beer] :
                #Choose only those customers who are similar for collaborative filtering.
                if record[CUSTOMER_ID] in self.similarCustomers :
                    sumOfRatings += float(record[REVIEW_OVERALL])
                    totalCount += 1
            if totalCount != 0 :
                avg[beer] = float(sumOfRatings / totalCount)
        return avg

    
start = default_timer()

#Build the initial matrix availableCustomerRows from the input data.
CSVDataLoader().transposeRowsColumns('C:/nus/cs5228 - kddm/predicteasy/data/beer_reviews.csv')

testCustomer = '2BDChicago'
testProduct = 'Heavy Handed IPA'

#Find Similar customers for this customer
print "Finding similar customers for : ", testCustomer
similarCustomers = knnc.findSimilarCustomers(testCustomer, availableCustomerRows, availableBeerColumns);

#Fnd all the beers which are similar to this one.
print "Finding similar beers for : ", testProduct
similarBeers = kv.findSimiarity(testProduct, availableBeerColumns, availableCustomerRows, FIELD_MAP)

filteredRating = 0
overallRating = 0
try :
    #BeerName - 'Heavy Handed IPA'
    model = PredictionModel(testCustomer, similarCustomers, similarBeers)

    #Next for each of those products find the common reviewers.
    baselineRating = model.computeGlobalBaseline(testProduct)

    print "Global BaseLine rating : ", baselineRating

    #Compute rating by Collaborative filtering.
    filteredRating = model.computeFilteredRatingEstimate('Heavy Handed IPA')
    for k,v in filteredRating.iteritems():
        print "rating for : ", k,  " is " , v
        overallRating += v;
    overallRating = (overallRating / len(filteredRating))
except Exception as e:
    print e
    pass

duration = default_timer() - start

print "Overall Rating for the combination : ", testCustomer, ", ", testProduct, " is : ", overallRating

print "Overall time taken to run the prediction : ", duration
