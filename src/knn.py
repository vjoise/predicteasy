###########################################################################################
#Implementing it here, since doing this on java requires lot of memory for record count > 1M might throw OOM.
#Generate the set of similar items by this logic.
#Parse Beer/product data and group the people who have reviewed products/beers.
#1. Get all the beers/products which have been reviewed by more than 1 person.
#2. Find all the reviews written by those common users.
#3. Now for the entire dataset, compute the weighted simiarity index of two beers at a time.
#4. Predict/Recommend the kind of beer according to the current ranking computed above, to the user.
###########################################################################################

import csv
import math
import operator

#This holds the rows in an array.
dataRow = []

#This map holds the groups of people who have reviewed the similar number of products.
#For example, reviewMap = {2, <array of people who have reviewed 2 products>}
#reviewMap = {3, <array of people who have reviewed 3 products>} and so on.
reviewMap={}

#reviewersMap = {itemName, [list of reviewers]}.
itemReviewersMap={}

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
FIELD_MAP['brewery_id'] = 12

REVIEW_MAP_KEY = 10 #beer_name
COMMON_REVIEWERS_MAP_KEY = 6 #review_profilename

#Put a list of items in the map value.
def putListMapEntry(key, value, inputMap) :
    v = inputMap.get(key)
    if v == None :
        v = []
    v.append(value)
    inputMap[key] = v

#This class loads data from the CSV on to an in-memory matrix.
class CSVDataLoader :
    def loadData(self, filePath) :
        csvOut = open(str(filePath), 'rb')
        reader = csv.reader(csvOut)
        count=0
        for data in reader :
            if count == 0:
                #Ignore the header and continue from the 2nd one.
                count= count + 1
                continue
            dataRow.append(data)
            putListMapEntry(data[REVIEW_MAP_KEY], data, reviewMap)
            putListMapEntry(data[REVIEW_MAP_KEY], data[COMMON_REVIEWERS_MAP_KEY], itemReviewersMap)
            count = count + 1
            if count > 100:
                break
        print "# of records = ", count
        
#Utility to find the similar items.
class SimilarItemsFinder:
    #We can compute distances on a set of features for a product.
    featureSet = []

    factorOfK = 1
    
    def __init__(self, features, factorOfK):
        self.featureSet = features
     
    #This method finds the similar items by calculating distances on different attributes.
    def findSimilarItems(self, item):

        #Initialize Similar items here
        similarItems = []

        # For all the items, compare this item on features and return the most closest matching items.
        for r in dataRow:

            #Skip KNN if it is the same beer.
            if r[REVIEW_MAP_KEY] == item :
                continue
            
            #First find the common reviewers for argument item and the item in loop.
            reviewerList = self.findCommonReviewers(r[REVIEW_MAP_KEY], item)

            #Find common reviewes for both left and right items.
            leftComparable  = r[REVIEW_MAP_KEY]
            rightComparable = item

            #Get the reviews for all the functions for argument item and the item in the for loop.
            leftReviews  = self.findReviews(leftComparable, reviewerList)
            rightReviews = self.findReviews(rightComparable, reviewerList)

            #Now let us compute the distance between these reviews.
            distance = self.computeDistance(leftReviews, rightReviews)
            distance['item'] = r[REVIEW_MAP_KEY]
            if len(distance) > 0:
                if not self.contains(similarItems, leftComparable):
                    similarItems.append(distance)
            
        return similarItems

    #Util method to check item existence in the list.
    def contains(self, itemList, item):
        for i in itemList :
            if i == item :
                return True
        

    #This will give the list of entries for a given field. (columnar data)
    def getFieldVector(self, records, field) :
        fieldVector = []
        for record in records :
            index = FIELD_MAP[field]
            fieldVector.append(record[index])
        return fieldVector
        
    #Calculate the actual distance (euclidean distance) between two items by comparing all the features.
    def computeDistance(self, listOne, listTwo):
        distanceMap = {}
        for feature in self.featureSet:
            #Get Vector 1 & 2 for this feature
            vector1 = self.getFieldVector(listOne, feature)
            vector2 = self.getFieldVector(listTwo, feature)
            #Initialize distance
            distance = 0
            calculated = 0
            for v1 in vector1 :
                n1 = float(v1)
                for v2 in vector2 :
                    n2 = float(v2)
                    distance += pow((n1 - n2), 2)
                    calculated = 1
            #Calculate the euclidean distance here.
            if calculated == 1:
                distanceMap[feature] = math.sqrt(distance)
        return distanceMap

    #Find the reviews for a bunch of reviewers for this item.
    def findReviews(self, item, listOfReviewers) :
        listOfReviews = []
        reviewsForItem = reviewMap.get(item)
        if self.notEmpty(reviewsForItem):
            for row in reviewsForItem:
                for reviewer in listOfReviewers : 
                    if row[COMMON_REVIEWERS_MAP_KEY] == reviewer :
                        listOfReviews.append(row)
        return listOfReviews

    #This will help us to club the groups of items by reviewers
    def findCommonReviewers(self, item1, item2) :
        commonReviewers = []
        reviewersOfItem1 = itemReviewersMap.get(item1)
        reviewersOfItem2 = itemReviewersMap.get(item2)
        if self.notEmpty(reviewersOfItem1) and self.notEmpty(reviewersOfItem2):
            for r1 in reviewersOfItem1:
                for r2 in reviewersOfItem2:
                    if r1 == r2 :
                       commonReviewers.append(r1)
        return commonReviewers

    def notEmpty(self, item1) :
        return item1 is not None and len(item1) > 0
        
def getNearestNeighbors(testQuery):
    LIST_OF_FEATURES = ['review_overall', 'review_aroma','review_appearance', 'review_palate', 'review_taste']
    nearestNeighborsMap = {}
    #Load the data first
    loader = CSVDataLoader()
    loader.loadData('C:/NUS/beer_reviews.csv')
    
    #once data is loaded find the similar items which have been reviewed.
    finder = SimilarItemsFinder(LIST_OF_FEATURES, math.sqrt(31))
    for query in testQuery :
        nearestNeighborsMap[query] = finder.findSimilarItems(query)
    return nearestNeighborsMap
    

#Test the prediction here.
testQuery = ['Caldera Ginger Beer']
knn=getNearestNeighbors(testQuery)

print "The list of similar items for ", testQuery, " are "

print len(knn)

if knn is not None :
    for k in knn :
        print knn[k]
