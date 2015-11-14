import csv
import math
import operator
import knn_beer as kv
import knn_customer as knnc
from timeit import default_timer

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
