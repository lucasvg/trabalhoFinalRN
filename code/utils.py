import datetime
import pandas as pd
import numpy as np
import time
import backtrader as bt

def calcMeanStd(label, arr):
    print(label + ': ' + str(np.mean(arr)) + '(+-' + str(np.std(arr)) + '), max: ' + str(np.max(arr)) + ', min: ' + str(np.min(arr)))
    print('calcMeanStd: ', arr)


def runBackTest(TESTS, NUMBER_OF_RUNS, TestStrategy, MySizer, DEFAULT_DT_FORMAT, DEFAULT_FROM_DATE):
    for test in TESTS:
        print('############################')
        print('starting', test['key'])
        print('############################')
        start = time.time()
        statisticsPerTest = []

        for runNumber in range(NUMBER_OF_RUNS):
            TestStrategy.clf = test["clf"]
            cerebro = bt.Cerebro(stdstats=True)
            cerebro.addstrategy(TestStrategy)
            cerebro.addsizer(MySizer)
            data = bt.feeds.GenericCSVData(
                dataname="../dataset/" + test['dataFileName'] +  ".csv",
                # dtformat=('%Y.%m.%d'),
                dtformat=test['dtformat'] if 'dtformat' in test else DEFAULT_DT_FORMAT,
                fromdate=test['fromDate'] if 'fromDate' in test else DEFAULT_FROM_DATE,
                openinterest=-1
            )

            cerebro.adddata(data)
            cerebro.broker.setcash(10000.0)
        
            #https://www.backtrader.com/docu/commission-schemes/commission-schemes/
            cerebro.broker.setcommission(commission=0, margin=False, mult=1.0, leverage=100) 

            results = cerebro.run()

            statistics = results[0] # for data0
            
            statisticsPerTest.append({
                'toMean': statistics.toMean,
                'portfolio': statistics.broker.getvalue(),
            })
            if(runNumber == 0):
                test['resultCerebro'] = cerebro
            print("end run", runNumber)


        testScoresPerTest = [np.mean(j['testScores']['data']) for j in [i['toMean'] for i in statisticsPerTest]]
        calcMeanStd('testScore', testScoresPerTest)
        calcMeanStd('portfolio', [i['portfolio'] for i in statisticsPerTest])

        end = time.time() 
        print('total execution time:', "%.2f" % (end-start))