from csv_loader import *
from prediction_model import *
import knn_beer as kv
import knn_customer as knnc
from timeit import default_timer
from util import *

start = default_timer()

#Build the initial matrix availableCustomerRows from the input data.
csvLoader = CSVDataLoader()
csvLoader.transposeRowsColumns('../../resources/beer_reviews.csv')

availableBeerColumns = csvLoader.getAvailableBeerColumns()
availableCustomerRows = csvLoader.getAvailableCustomerRows() 

testQueries = [['rawthar' , 'Caldera Ginger Beer', 4.0], ['Halcyondays' , 'Caldera Ginger Beer', 4.0]]

actualToPredictedRating = []

for query in testQueries :

	testCustomer = query[0]
	testProduct = query[1]
	actualRating = query[2]
	print "****************************************"
	print "Test Query ", query
	
	#Step 1 : Find Similar customers for this customer
	print "Finding similar customers for : ", testCustomer
	similarCustomers = knnc.findSimilarCustomers(testCustomer, availableCustomerRows, availableBeerColumns);
	
	#Step 2 : Fnd all the beers which are similar to this one.
	print "Finding similar beers for : ", testProduct
	#similarBeers = kv.findSimiarityInParallel(testProduct, availableBeerColumns, availableCustomerRows, FIELD_MAP)
	similarBeers = kv.findSimiarity(testProduct, availableBeerColumns, availableCustomerRows, FIELD_MAP)

	#Step 3 : Predict rating for this query
	filteredRating = 0
	overallRating = 0
	
	try :
	    #BeerName - 'Heavy Handed IPA'
	    model = PredictionModel(testCustomer, similarCustomers, similarBeers, availableBeerColumns, availableCustomerRows)
	
	    #Next for each of those products find the common reviewers.
	    print "Finding Global BaseLine rating..."
	    baselineRating = model.computeGlobalBaseline(testProduct)
	    print "Global BaseLine rating : ", baselineRating
	
	    #Compute rating by Collaborative filtering.
	    print "Finding filtered rating..."
	    filteredRating = model.computeFilteredRatingEstimate(testProduct)
	    print "Filtered rating : ", filteredRating
	
	    #Now get the average overall rating
	    for k,v in filteredRating.iteritems():
	        #print "rating for : ", k,  " is " , v
	        overallRating += v;
	        
	    overallRating = (overallRating / len(filteredRating))
	    print "Overall Rating : ",  overallRating
	    print "****************************************"
	    
	    actualToPredictedRating.append([actualRating] + [overallRating])
	
	except Exception as e:
	    print e
	    pass


def computeRMSError(actualToPredictedRatingArr):
	rmSqError = 0
	print actualToPredictedRatingArr
	for key in actualToPredictedRatingArr :
		rmSqError += math.pow((key[0] - key[1]), 2)
	
	return (math.sqrt (rmSqError) / len(actualToPredictedRatingArr))
	
		
#get Root mean square error
rmSqError = computeRMSError(actualToPredictedRating)
print "Aggregated Root mean square error : ", rmSqError

duration = default_timer() - start

print "Overall Rating for the combination : ", testCustomer, ", ", testProduct, " is : ", overallRating

print "Overall time taken to run the prediction : ", duration
