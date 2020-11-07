import datetime
import pandas as pd
from sklearn.preprocessing import MaxAbsScaler

# ENUM
UP = 1
DOWN = 0

def getDataFromIndicatorsForPrediction(amount, indicators):
    data = []
    for i in range(-1*(amount-1), 1):
        line = []
        for indicator in indicators:
            line.append(indicator[i])
        data.append(line)
    data = MaxAbsScaler().fit_transform(data).tolist()
    return data

def generateTarget(backTestingData, amount, threshold = 0):
    target =  []
    for i in range(-1*(amount-1), 1):
        if ((backTestingData.close[i+1]-backTestingData.close[i]) >= 0):
            target.append(UP)
        else:
            target.append(DOWN)
    return target

def prepareDataForTraining(backTestingData, amount, threshold, indicators):
    target = generateTarget(backTestingData, amount+1, threshold)
    data = getDataFromIndicatorsForPrediction(amount+1, indicators)
    target.pop() # removes today from trainingData
    data.pop() # removes today from trainingData
    return data, target
