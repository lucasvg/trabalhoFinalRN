import datetime
import pandas as pd
import numpy as np
import time
import backtrader as bt
import ast

def calcMeanStd(label, arr):
    print(label + ': ' + str(np.mean(arr)) + '(+-' + str(np.std(arr)) + '), max: ' + str(np.max(arr)) + ', min: ' + str(np.min(arr)))
    print('calcMeanStd: ', arr)

def runBackTest(TESTS, NUMBER_OF_RUNS, DEFAULT_DT_FORMAT, DEFAULT_FROM_DATE):
    f = open('../dataset/compiled/data_1500.txt', 'r') 
    lines = f.readlines() 
    data = [ast.literal_eval(i) for i in lines]

    for test in TESTS:
        print('############################')
        print('starting', test['key'])
        print('############################')
        start = time.time()
        statisticsPerTest = []

        for runNumber in range(NUMBER_OF_RUNS):
            statisticsPerTest.append(runTest(test, data))
            print("end run", runNumber)

        testScoresPerTest = [np.mean([i['accuracy'] for i in statisticsPerTest])]
        calcMeanStd('testScore', testScoresPerTest)

        end = time.time() 
        print('total execution time:', "%.2f" % (end-start))

def runTest(test, dataset):
    clf = test['clf']

    SIZE_OF_TRAINING_DATA = 1500
    SIZE_OF_PREDICT_DATA = 1

    if(len(dataset[0][0]) != SIZE_OF_TRAINING_DATA):
        raise Exception('first data should be for training')

    result = []
    for data in dataset:
        target = data[1]
        data = data[0]
        if(len(data) == SIZE_OF_PREDICT_DATA): # to predict
            result.append([ clf.predict(data)[0], target[0] ])
        elif(len(data) == SIZE_OF_TRAINING_DATA): # to train
            clf.fit(data, target)
        else:
            raise Exception('unhandled case')


    correctPredictions = 0
    wrongPredictions = 0
    for i in result:
        if(i[0] == i[1]):
            correctPredictions+=1
        else:
            wrongPredictions+=1
    accuracy = correctPredictions/(correctPredictions+wrongPredictions)
    
    return {
        'correctPredictions': correctPredictions,
        'wrongPredictions': wrongPredictions,
        'accuracy': accuracy
    }