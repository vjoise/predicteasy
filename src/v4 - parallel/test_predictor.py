from csv_loader import *
from prediction_model import *
import knn_beer as kv
import knn_customer as knnc
from timeit import default_timer
import concurrent.futures

sumOfBeerRatingsOverall = 0
availableBeerColumns = {}
availableCustomerRows = {}
csvLoader = CSVDataLoader()

#Build the initial matrix availableCustomerRows from the input data.

partitionSize = 1000000

def getHugeData(filePath) :
        csvOut = open(str(filePath), 'r')
        reader = csv.reader(csvOut)
        count = 0
        for record in reader :
            yield record
            count += 1


def processData(count, availableBeerColumns, availableCustomerRows, sumOfBeerRatingsOverall):
    MEAN_PRODUCT_RATING=round((sumOfBeerRatingsOverall/count), 1)
    print ("Mean Beer rating for any beer : ", MEAN_PRODUCT_RATING)
    print ("# of beers = ", len(availableBeerColumns))
    print ("# of customers = ", len(availableCustomerRows))
    
        #availableBeerColumns = csvLoader.getAvailableBeerColumns()
        #availableCustomerRows = csvLoader.getAvailableCustomerRows() 

    #Demo - combined run
    #testQueries = [['rawthar' , 'Caldera Ginger Beer', 4.0], ['Halcyondays' , 'Caldera Ginger Beer', 4.0],['rawthar' , 'Heavy Handed IPA', 4.0] ]

    #Demo - quick run
    testQueries = [['hopdog' , 'Iron Hill Northern English Brown Ale', 3.0]]

    #Demo - large data

    #testQueries = [['rawthar' , 'Heavy Handed IPA', 4.0]]
    #, ['Halcyondays' , 'Caldera Ginger Beer', 4.0]]
    #testQueries = [['stcules', 'English Strong Ale',3.0]]

    actualToPredictedRating = []

    for query in testQueries :

        testCustomer = query[0]
        testProduct = query[1]
        actualRating = query[2]
        print ("****************************************")
        print ("Test Query ", query)
        
        #Step 1 : Find Similar customers for this customer
        print ("Finding similar customers for : ", testCustomer)
        similarCustomers = knnc.findSimilarCustomers(testCustomer, availableCustomerRows, availableBeerColumns);

        print ("SIMILAR Customers *****", len(similarCustomers))
        
        #Step 2 : Fnd all the beers which are similar to this one.
        print ("Finding similar beers for : ", testProduct)
        similarBeers = kv.findSimiarityInParallel(testProduct, availableBeerColumns, availableCustomerRows, FIELD_MAP)
        #similarBeers = kv.findSimiarity(testProduct, availableBeerColumns, availableCustomerRows, FIELD_MAP)

        #print ("SIMILAR ONES *****", similarBeers[0])

        #Step 3 : Predict rating for this query
        filteredRating = 0
        overallRating = 0
        
        try :
            #BeerName - 'Heavy Handed IPA'
            model = PredictionModel(testCustomer, similarCustomers, similarBeers, availableBeerColumns, availableCustomerRows)
        
            #Next for each of those products find the common reviewers.
            print ("Finding Global BaseLine rating...")
            baselineRating = model.computeGlobalBaseline(testProduct)
            print ("Global BaseLine rating : ", baselineRating)
        
            #Compute rating by Collaborative filtering.
            print ("Finding filtered rating...")
            filteredRating = model.computeFilteredRatingEstimate(testProduct)
            
            #Now get the average overall rating
            for k,v in filteredRating.items():
                #print "rating for : ", k,  " is " , v
                overallRating += v;
            if len(filteredRating) == 0 :
                print ("Cannot predict overall rating, as filtered rating is zero!");
                break
            overallRating = (overallRating / len(filteredRating))
            print ("Overall Rating : ",  overallRating)
            print ("****************************************")
            
            actualToPredictedRating.append([actualRating] + [overallRating])
        
        except Exception as e:
            print (e)
            pass
        
        return actualToPredictedRating

def avg(ratings):
        sum = 0
        count = 0
        print ("Rating value : ", ratings)
        for rating in ratings :
                if len(rating) == 2:
                        sum += rating[1]
                        count += 1
        if count == 0 :
                return 0
        return (sum / count)

def fun() :
    start_time = default_timer()
    sumOfBeerRatingsOverall = 0
    count=0
    ratingsForAllPartitions = []
    #recordCount += partitionSize
    availableBeerColumns = {}
    availableCustomerRows = {}
    print ("Loading Data Partitions...")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
    for data in getHugeData("c:/nus/data/ratebeer.csv") :
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
        if count <= partitionSize :
                continue
        count += 1
        print ("availableBeerColumns = {}", len(availableBeerColumns))
        print ("availableCustomerRows = {}", len(availableCustomerRows))
        print ("loaded completely...")
        cumulativeRatingTillNow = processData(count, availableBeerColumns, availableCustomerRows, sumOfBeerRatingsOverall)
        for i in cumulativeRatingTillNow:
                ratingsForAllPartitions.append(i)
        #Re-initialize these maps.
        availableBeerColumns = {}
        availableCustomerRows = {}
        count = 0
        print ("Cumulative Rating for this partition : ", cumulativeRatingTillNow)
        print ("Average rating till now : ", avg(ratingsForAllPartitions))
        print ("Time spent till now :: ", (default_timer() - start_time) ,  " seconds ")
    #Calculate the RMS for all the records now.
    computeRMSError(ratingsForAllPartitions)
        

def computeRMSError(actualToPredictedRatingArr):
    rmSqError = 0
    if len(actualToPredictedRatingArr) == 0:
        print ("Cannot predict for this combination!")
        return
    for key in actualToPredictedRatingArr :
        rmSqError += math.pow((key[0] - key[1]), 2)
    return (math.sqrt (rmSqError) / len(actualToPredictedRatingArr))
        
            
    #get Root mean square error
    rmSqError = computeRMSError(actualToPredictedRating)
    print ("Aggregated Root mean square error : ", rmSqError)

    duration = default_timer() - start

    print ("Overall Rating for the combination : ", testCustomer, ", ", testProduct, " is : ", overallRating)

    print ("Overall time taken to run the prediction : ", duration)

fun()
