#This is a converter from input data to a review matrix
#Columns -> Beers
#Rows    -> Customers
import csv
import math
import operator
from threading import *

CUSTOMER_ID = 6 #review_profilename
BEER_NAME = 10 #beer_name
REVIEW_OVERALL = 3 #review_overall
COMMON_REVIEWERS_MAP_KEY = 6

#Find people who have reviewed these two beers in comparison.
def reviewersOfBeer(beer, beersMap):
    reviewers = []
    for row in beersMap.get(beer):
        #Just to make sure there are no duplicate users.
        customer = row[CUSTOMER_ID]
        if customer not in reviewers :
            reviewers.append(customer);
    return reviewers;

def intersect(r1, r2):
    bigSet = []
    for i in r1 :
        if i in r2:
            bigSet.append(i)
    return bigSet


def findCommonReviewers(beer1, beer2, beersMap, peopleMap):
    beer1Reviewers = reviewersOfBeer(beer1, beersMap);
    beer2Reviewers = reviewersOfBeer(beer2, beersMap);
    #Now find the common reviewers of both beers
    return intersect(beer1Reviewers, beer2Reviewers)
        
        
def computeDistance(self, testData, data) :
    distance = 0
    for key,value in testData.getFeatures().iteritems() :
        leftValue = float(value)
        rightValue = float(data[FIELD_MAP[key]])
        distance += pow((leftValue- rightValue), 2)
    return math.sqrt(distance)

#Method to get the reviews done by the users.
def getReviews(beer, reviewers, beersMap):
    reviews = []
    for r in beersMap.get(beer) :
        customer = r[CUSTOMER_ID]
        if customer in reviewers:
            reviews.append(r)
    return reviews

#Calculate Distance
FEATURE_SET = ['review_overall', 'review_aroma', 'review_palate', 'review_taste']

def computeDistance(testData, data) :
    distance = 0
    leftValue = float(testData)
    rightValue = float(data)
    distance = pow((leftValue- rightValue), 2)
    return math.sqrt(distance)

def calculate_similarity(beer1, beer2, beersMap, peopleMap, FIELD_MAP):
    
    #First find common reviewers
    reviewers = findCommonReviewers(beer1, beer2, beersMap, peopleMap)

    # Now get the reviews done by those common users
    b1Reviews = getReviews(beer1, reviewers, beersMap)
    b2Reviews = getReviews(beer2, reviewers, beersMap)

    #Now calculate the distance between them
    dists = []
    
    for b1r in b1Reviews :
        for b2r in b2Reviews :
            for f in FEATURE_SET:
                dists.append(computeDistance(b1r[FIELD_MAP[f]], b2r[FIELD_MAP[f]]))
    return dists

#Calculate similarity of set of beers
def findSimiarity(testBeer, beersMap, peopleMap, FIELD_MAP):
    dist = []
    count = 0
    returnList = []
    for beer in beersMap.keys():
        if count % 1000 == 0 :
            print "\nprocessing batch :: ", count
        if beer != testBeer:
           similarity = calculate_similarity(testBeer, beer, beersMap, peopleMap, FIELD_MAP)
           distance = 99999
           if similarity is not None and len(similarity) > 0 :
               distance = similarity[0]
           row = [testBeer, beer] + [distance]
           dist.append(row)
        count = count + 1
    dist.sort(key=operator.itemgetter(2))
    
    k = math.sqrt(len(dist))
    for item in range(0, int(k-1)):
    	returnList.append(dist[item][1])
    	
   	return returnList

class SimilarItemsFinderThread(Thread) :
    testBeer  = ''
    tempMap   = {}
    peopleMap = {}
    FIELD_MAP = {}
    def __init__(self, testBeer, tempMap, peopleMap, FIELD_MAP):
        self.testBeer = testBeer
        self.tempMap = tempMap
        self.peopleMap = peopleMap
        self.FIELD_MAP = FIELD_MAP
        Thread.__init__(self)
        
    def run(self):
        findSimiarity(self.testBeer, self.tempMap, self.peopleMap, self.FIELD_MAP)
    

#Calculate similarity of set of beers
def findSimiarityInParallel(testBeer, beersMap, peopleMap, FIELD_MAP):
    dist = []
    count = 0
    rowCount = 0
    batchSize = len(beersMap) / 10
    print "Batch Size is : ", batchSize
    beersPartitionMap = {}
    finders = []
    batchNumber = 0
    tempMap = {}
    for k,v in beersMap.iteritems() :
        tempMap[k] = v
        if rowCount % batchSize == 0:
            print "starting batch : ", batchNumber
            finder = SimilarItemsFinderThread(testBeer, beersMap, peopleMap, FIELD_MAP)
            finder.start()
            finders.append(finder)
            batchNumber += 1
        rowCount += 1
    for f in finders :
        f.join()
    
