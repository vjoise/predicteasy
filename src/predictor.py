######################################################################
# Prediction Runner test client
######################################################################

import knn_numeric
from predictionmodel import PredictionModel
from predictionquery import PredictionQuery
from timeit import default_timer
import csv

class PredictionRunner :
 
    def __init__(self, features, kValue):
        self.featureSet = features
        self.factorOfK = kValue 
 


#Construct a Query first.
LIST_OF_FEATURES = ['review_overall', 'review_aroma','review_appearance', 'review_palate', 'review_taste']

#Test the prediction here.
#Prediction query can be on multiple fields, we can pass in values for the above feature list and predict whether the prediction holds good or not.
testQuery = PredictionQuery()

#For a similar beer, predict the overall rating.

#testQuery.addFeature('brewery_id', 42) #'The Stable' 4	3.5	3.5
testQuery.addFeature('review_overall', 2)
testQuery.addFeature('review_aroma', 2)
testQuery.addFeature('review_palate', 2)
testQuery.addFeature('review_appearance', 3)
testQuery.addFeature('review_taste', 2)
testQuery.addFeature('beer_name','castle')
testQuery.setQueryFeatures(['beer_name', 'beer_style']) #Amalgamated Dunkel


start = default_timer()

kNNList = knn_numeric.getNearestNeighbors(testQuery)

knnFile = "C:/NUS/knn.csv"
csvOut = open(knnFile, 'wb')
writer = csv.writer(csvOut)

writer.writerows(kNNList)

duration = default_timer() - start

#print 'Last record is : ', kNNList[len(kNNList) - 1]

#def verifyItemInKNN():
#    found = False
#    for item in kNNList:
#        if int(item[0]) == 42:
#            print "Item present in the KNN : ", item
#            found = True
#    if not found :
#        print "Couldn't find the item specified : ", testQuery

#verifyItemInKNN()

print "Total time taken : ", duration, " seconds ", " with # of records : ", len(kNNList)

predictionModel = PredictionModel(kNNList)

predictionModel.predict(testQuery)

#Get the Nearest Neighbors
