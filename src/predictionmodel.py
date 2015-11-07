######################################################################
#This is a prediction model for the given set of KNNs and a test query
#The prediction will be done on the missing input parameter.
#The model instance can be different for different kinds of input query.
######################################################################

class PredictionModel:
    listOfKNN = []

    def __init__(self, listOfKNN):
        self.listOfKNN = listOfKNN
        self.construct()
        
    def construct(self):
        print "Constructing a model based on the prediction query"
        #For all the rows in the generated KNN
        #for row in listOfKNN :
        #    for innerRow in listOfKNN :
        #        self.compareValues()

    def compareTwoVectors(dependent, independent):
        #increasing or decreasing functions f(vector1)
        for v in independent :
            pass
    
                        
    def predict(self, testQuery):
        print "Predicting for ", testQuery
