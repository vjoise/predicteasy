from csv_loader import *
from prediction_model import *
import knn_beer as kv
import knn_customer as knnc
from timeit import default_timer
from util import *

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
similarBeers = kv.findSimiarityInParallel(testProduct, availableBeerColumns, availableCustomerRows, FIELD_MAP)

filteredRating = 0
overallRating = 0
try :
    #BeerName - 'Heavy Handed IPA'
    model = PredictionModel(testCustomer, similarCustomers)

    #Next for each of those products find the common reviewers.
    baselineRating = model.computeGlobalBaseline(testProduct)

    print "Global BaseLine rating : ", baselineRating

    #Compute rating by Collaborative filtering.
    filteredRating = model.computeFilteredRatingEstimate(testProduct)

    #Now get the average overall rating
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
