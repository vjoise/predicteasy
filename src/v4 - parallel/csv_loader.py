import csv
import math
import operator
from timeit import default_timer

FIELD_MAP = {}
FIELD_MAP['beer_name'] = 0
FIELD_MAP['beer_id'] = 1
FIELD_MAP['brewer_id'] = 2
FIELD_MAP['review_overall'] = 9
FIELD_MAP['review_aroma'] = 6
FIELD_MAP['review_appearance'] = 5
FIELD_MAP['review_profilename'] = 11
FIELD_MAP['beer_style'] = 4
FIELD_MAP['review_palate'] = 7
FIELD_MAP['review_taste'] = 8


CUSTOMER_ID = 11 #review_profilename
BEER_NAME = 0 #beer_name
REVIEW_OVERALL = 9 #review_overall

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


#This class loads data from the CSV on to an in-memory matrix.
class CSVDataLoader :
    
    def getHugeData(self, filePath) :
        csvOut = open(str(filePath), 'r')
        reader = csv.reader(csvOut)
        print ("loaded completely...")
        count = 0
        for record in reader :
            #if count % 100000 == 0 :
            #    print ("Processing :: ", count)
            yield record
            count += 1 
            
    def transposeRowsColumns(self, filePath, partitionSize) :
        start_time = default_timer()
        sumOfBeerRatingsOverall = 0
        count=0
        for data in self.getHugeData(filePath) :
            if count >= partitionSize :
                return
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
        print ("Time taken to load data : ", (default_timer() - start_time))
        print ("Mean Beer rating for any beer : ", MEAN_PRODUCT_RATING)
        print ("# of beers = ", len(availableBeerColumns))
        print ("# of customers = ", len(availableCustomerRows))
    
    def getAvailableCustomerRows(self) :
    	return availableCustomerRows    
    
    def getAvailableBeerColumns(self) :
    	return availableBeerColumns  
    	     
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
