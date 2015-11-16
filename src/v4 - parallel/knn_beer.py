#This is a converter from input data to a review matrix
#Columns -> Beers
#Rows    -> Customers
import csv
import math
import operator
from threading import *
import concurrent.futures


CUSTOMER_ID = 6 #review_profilename
BEER_NAME = 10 #beer_name
REVIEW_OVERALL = 3 #review_overall
COMMON_REVIEWERS_MAP_KEY = 6

#Find people who have reviewed these two beers in comparison.
def reviewersOfBeer(beer, beersMap):
    reviewers = []
    allRatings = beersMap.get(beer)
    if allRatings is None :
        return []
    for row in allRatings:
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
    allRatings = beersMap.get(beer)
    if allRatings is None :
        return []
    for r in allRatings :
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
    #print ("Similarity CalCULATION >>>>>>>>>>>>>>", beer1, beer2)
    #First find common reviewers
    reviewers = findCommonReviewers(beer1, beer2, beersMap, peopleMap)
    
    # Now get the reviews done by those common users
    b1Reviews = getReviews(beer1, reviewers, beersMap)
    b2Reviews = getReviews(beer2, reviewers, beersMap)
    #print ("b1Reviews", b1Reviews)
    #print ("b2Reviews", b2Reviews)
    #Now calculate the distance between them
    dists = []    
    for b1r in b1Reviews :
        for b2r in b2Reviews :
            for f in FEATURE_SET:
                dists.append(computeDistance(b1r[FIELD_MAP[f]], b2r[FIELD_MAP[f]]))
    return dists

#Calculate similarity of set of beers
def findSimiarity(testBeer, beersMap, peopleMap, FIELD_MAP, lock):
    #lock.acquire() 
    dist = []
    #print ("Acquired Lock ", lock)
    count = 0
    returnList = []
    #print "TestBeer ****** ", testBeer
    #print "People map ***** ", peopleMap
    #print("BeerMap Lenght ish " , len(beersMap))
    for beer in beersMap.keys():
        if count % 10000 == 0 :
            print ("\nprocessing batch :: ", count)
        if beer != testBeer:
           #print ("Test beer", testBeer, " User Beer : ", beer)
           similarity = calculate_similarity(testBeer, beer, beersMap, peopleMap, FIELD_MAP)
           distance = 99999
           if similarity is not None and len(similarity) > 0 :
               distance = similarity[0]
           row = [testBeer, beer] + [distance]
           dist.append(row)
        count = count + 1
    dist.sort(key=operator.itemgetter(2))
    
    k = math.sqrt(len(dist))
    if k > 1:
        for item in range(0, int(k-1)):
            returnList.append(dist[item][1])
    	
    #lock.release()
    
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
    batchSize = int(len(beersMap) / 10)
    if batchSize == 0 :
        batchSize = 1
    print ("Batch Size is : ", batchSize)
    beersPartitionMap = {}
    finders = []
    batchNumber = 0
    tempMap = {}
    tempArray = []
    for k,v in beersMap.items() :
        tempMap[k] = v
        if rowCount % batchSize == 0:
            print ("starting batch : ", batchNumber)
            tempArray.append(tempMap)
            tempMap = {}
            batchNumber += 1
        rowCount += 1
    print ("Len of tempArray is :: ", len(tempArray))
    lock = RLock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=batchSize) as executor:
        finders = [executor.submit(findSimiarity, testBeer, tempMap, peopleMap, FIELD_MAP, lock) for tempMap in tempArray]
    #print([finders.result() for fut in concurrent.futures.as_completed(finders)])
        
    print ("Waiting for individual data now...")
    for future in concurrent.futures.as_completed(finders):
        try:
            data = future.result()
            for d in data:
                if d not in dist:
                    dist.append(d)
        except Exception as exc:
            print('generated an exception:', exc)
    return dist
    
