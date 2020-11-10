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
            cerebro = bt.Cerebro(stdstats=False)
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

            cerebro.addobserver(bt.observers.Value)
            cerebro.addobserver(bt.observers.Trades)
            cerebro.addobserver(bt.observers.BuySell)

            cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')

            results = cerebro.run()

            statistics = results[0] # for data0

            print(str(statistics.analyzers.TradeAnalyzer.get_analysis()))

            correctPredictions = 0
            wrongPredictions = 0
            for i in statistics.toMean['predictions']:
                if(i[0] == i[1]):
                    correctPredictions+=1
                else:
                    wrongPredictions+=1
            accuracy = correctPredictions/(correctPredictions+wrongPredictions)
            statistics.toMean['accuracy'] = accuracy
            print(str({
                'accuracy': accuracy,
                'correctPredictions': correctPredictions,
                'wrongPredictions': wrongPredictions
            }))
            
            statisticsPerTest.append({
                'toMean': statistics.toMean,
                'portfolio': statistics.broker.getvalue(),
            })
            
            if(runNumber == 0):
                test['resultCerebro'] = cerebro
            print("end run", runNumber)

        accuracy = [i['toMean']['accuracy'] for i in statisticsPerTest]
        calcMeanStd('accuracy', accuracy)
        
        calcMeanStd('portfolio', [i['portfolio'] for i in statisticsPerTest])

        end = time.time() 
        print('total execution time:', "%.2f" % (end-start))