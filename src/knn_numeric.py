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

#For concurrent execution of kNN search
import concurrent.futures

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
FIELD_MAP['beer_id'] = 12

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
            #if count > 100:
            #    break
        print "# of records = ", count
        
#Utility to find the similar items.
class SimilarItemsFinder:
    
    factorOfK = 1
    
    def __init__(self, kValue):
        self.factorOfK = kValue
     
    #This method finds the similar items by calculating distances on different attributes.
    def findSimilarItems(self, testRecord):

        #Initialize Similar items here
        similarItems = []
        distanceList = []
        processedRecordsMap = {}

        # For all the items, compare this item on features and return the most closest matching items.
        for rec in dataRow:

            #This is to remove duplicate beer_name's from the list.
            if processedRecordsMap.get(rec[FIELD_MAP['beer_name']]) is not None:
                continue

            processedRecordsMap[rec[FIELD_MAP['beer_name']]] = 1
                              
            #Since we do not know the order of input query, we need to loop through the key value pairs.
            dist = self.computeDistance(testRecord, rec)
            distanceList.append((dist, rec))
            
        distanceList.sort(key=operator.itemgetter(0))
        for item in range(self.factorOfK):
                similarItems.append(distanceList[item][1])
        return similarItems
    
    def computeDistance(self, testData, data) :
        distance = 0
        for key,value in testData.getFeatures().iteritems() :
            leftValue = float(value)
            rightValue = float(data[FIELD_MAP[key]])
            distance += pow((leftValue- rightValue), 2)
        return math.sqrt(distance)



#To get the nearest neighbors computed through the above logic.
def getNearestNeighbors(testQuery):
    nearestNeighborsMap = {}
    #Load the data first
    loader = CSVDataLoader()
    loader.loadData('C:/NUS/beer_reviews.csv')
    
    #once data is loaded find the similar items which have been reviewed.
    finder = SimilarItemsFinder(int(math.sqrt(len(dataRow))))
    
    return finder.findSimilarItems(testQuery)


