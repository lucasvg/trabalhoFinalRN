import datetime
import pandas as pd

def getDataFromIndicatorsForPrediction(amount, indicators):
    data = []
    for i in range(-1*(amount-1), 1):
        line = []
        for indicator in indicators:
            line.append(indicator[i])
        data.append(line)
    return data

def generateTarget(backTestingData, amount, threshold = 0):
    target =  []
    for i in range(-1*(amount-1), 1):
        if ((backTestingData.close[i+1]-backTestingData.close[i])/backTestingData.close[i] >= threshold):
            target.append(2)
        elif ((backTestingData.close[i+1]-backTestingData.close[i])/backTestingData.close[i] <= -threshold):
            target.append(0)
        else:
            target.append(1)
    return target

def prepareDataForTraining(backTestingData, amount, threshold, indicators):
    target = generateTarget(backTestingData, amount+1, threshold)
    data = getDataFromIndicatorsForPrediction(amount+1, indicators)
    target.pop() # removes today from trainingData
    data.pop() # removes today from trainingData
    return data, target
