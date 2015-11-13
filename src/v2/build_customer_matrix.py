#This is a converter from input data to a review matrix
#Columns -> Beers
#Rows    -> Customers
import csv
import math
import operator
import knnv2 as kv
import knn_customer as knnc
from timeit import default_timer


##############################################################################
#FIELD INDEX in the CSV
##############################################################################
FIELD_MAP = {}
FIELD_MAP['brewery_id'] = 0
FIELD_MAP['brewery_name'] = 1
FIELD_MAP['review_time'] = 2
FIELD_MAP['review_overall'] = 3
FIELD_MAP['review_aroma'] = 4
FIELD_MAP['review_appearance'] = 5
FIELD_MAP['review_profilename'] = 6
FIELD_MAP['beer_style'] = 7
FIELD_MAP['review_palate'] = 8
FIELD_MAP['review_taste'] = 9
FIELD_MAP['beer_name'] = 10
FIELD_MAP['beer_abv'] = 11
FIELD_MAP['beer_id'] = 12

CUSTOMER_ID = 6 #review_profilename
BEER_NAME = 10 #beer_name
REVIEW_OVERALL = 3 #review_overall
COMMON_REVIEWERS_MAP_KEY = 6

availableBeerColumns={}
availableCustomerRows={
    #Rating data can be used here.
    #'cust1' : {
    #            'ABC' : [3, 5] #review array[alcohol content, overall]
    #          }
}
dataRow = []

MEAN_PRODUCT_RATING = 0

similarProducts = []

class RatingData :
    product = ''
    overallRating = 0.0
    attributes = {}
    def __init__(self, product, overall, attributes) :
        self.product = product
        self.overallRating = overall
        self.attributes = attributes

#Put a list of items in the map value.
def putListMapEntry(key, value, inputMap) :
    v = inputMap.get(key)
    if v == None :
        v = []
    v.append(value)
    inputMap[key] = v

#This class loads data from the CSV on to an in-memory matrix.
class CSVDataLoader :
    def transposeRowsColumns(self, filePath) :
        start_time = default_timer()
        sumOfBeerRatingsOverall = 0
        csvOut = open(str(filePath), 'rb')
        reader = csv.reader(csvOut)
        count=0
        for data in reader :
            if count == 0:
                #Ignore the header and continue from the 2nd one.
                count= count + 1
                continue
            putListMapEntry(data[BEER_NAME], data, availableBeerColumns)
            ratingData = RatingData(data[BEER_NAME], data[REVIEW_OVERALL], {'beer_style' : data[FIELD_MAP['beer_style']]})
            putListMapEntry(data[CUSTOMER_ID], ratingData, availableCustomerRows) #Build a map of customer review list.
            count = count + 1
            sumOfBeerRatingsOverall += float(data[REVIEW_OVERALL])
            #if count == 100000 :
            #    break;
        MEAN_PRODUCT_RATING=round((sumOfBeerRatingsOverall/count), 1)
        print "Time taken to load data : ", (default_timer() - start_time)
        print "Mean Beer rating for any beer : ", MEAN_PRODUCT_RATING
        print "# of beers = ", len(availableBeerColumns)
        print "# of customers = ", len(availableCustomerRows)
        

#This is a class to compute global + collaborative values.
class PredictionModel :

    testCustomer = ''
    similarCustomers = []
    baselineEstimate = 0
    
    def __init__ (self, testCustomer, similarCustomers):
        self.testCustomer = testCustomer
        self.similarCustomers = similarCustomers
        
    inputData=[]
    
    def computeGlobalBaseline(self, productName):
        #Mean rating across all beers
        print "Overall Rating : ", MEAN_PRODUCT_RATING
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
        #Now find all the beers which are similar to this one.
        similarBeers = kv.findSimiarity(productName, availableBeerColumns, availableCustomerRows, FIELD_MAP)
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

    
    
def findSimilarCustomers(customerId) :
    return knnc.findSimilarCustomers(customerId, availableCustomerRows, availableBeerColumns);

    
start = default_timer()

#Build the initial matrix availableCustomerRows from the input data.
CSVDataLoader().transposeRowsColumns('C:/nus/cs5228 - kddm/predicteasy/data/beer_reviews.csv')

#Now find the similar customers for a given customer on a number of parameters.
#Choose any test profile to find its NN.

testCustomer = '2BDChicago'
testProduct = 'Heavy Handed IPA'

print "test Customer : ", testCustomer

print "test Product : ", testProduct

similarCustomers = findSimilarCustomers(testCustomer)
print "similar Customers for ", testCustomer, " :: "
print similarCustomers
#similarCustomers = ["stcules", "t420o"]
filteredRating = 0
overallRating = 0
try :
        
    #BeerName - 'Heavy Handed IPA'
    model = PredictionModel(testCustomer, similarCustomers)

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
