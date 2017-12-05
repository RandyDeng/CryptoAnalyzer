import numpy as np
from pyspark import SparkContext
from pymongo import MongoClient

client = MongoClient()
db = client.FinalDB
collection = db.Aggregations
sc = SparkContext('local',"Simple App")
data = sc.textFile('bitcoin_history/bitstampUSD.csv')
fromEpoch = int(sys.argv[1]) 
#1315922000
HourEpoch= fromEpoch + 3600
DayEpoch= fromEpoch + 86400
WeekEpoch= fromEpoch + 604800
MonthEpoch= fromEpoch + 2629743
#1315922024
MonthFiltered = data.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= MonthEpoch)).collect()
WeekFiltered = MonthFiltered.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= WeekEpoch)).collect()
DayFiltered = WeekFiltered.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= DayEpoch)).collect()
HourFiltered = DayFiltered.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= HourEpoch)).collect()
FilteredSets=[MonthFiltered,WeekFiltered,DayFiltered,HourFiltered]
count=1
for Set in FilterredSets:
    PriceList=[]
    for x in Set:
        PriceList.append(float(str(x).split(",")[1]))
    RunningAverage = np.convolve(PriceList, np.ones((2,))/2, mode='valid')
    print(result)
    if(count==1):
        toEpoch=MonthEpoch
        N=3000
    elif(count==2):
        toEpoch=WeekEpoch
        N=1500
    elif(count==3):
        toEpoch=DayEpoch
        N=300
    elif(count==4)
        toEpoch=HourEpoch
        N=25
    RunningAverage = np.convolve(PriceList, np.ones((N,))/N, mode='valid')
    weights = np.exp(np.linspace(-1, 0, N))
    ExponentialAverage = np.convolve(PriceList, weights / weights.sum(), mode='valid')[:len(PriceList)]
    ExponentialAverage[:N] = ExponentialAverage[N]
    moments = np.zeros((len(PriceList),))
    counter = 0
    last_data = 0
    for current_data in data:
        if counter == 0:
            moments[counter] = 0
        else:
            moments[counter] = moments[counter - 1] + (current_data - last_data) * F
            last_data = current_data
        counter++
    post = {"FromEpoch": fromEpoch,
             "ToEpoch": toEpoch,
             "RunningAverage": list(RunningAverage),
             "ExponentialAverage": list(ExponentialAverage),
             "MomentumLine": list(moments)}
    collection.insert_one(post)
    count=count+1

#submit this script with spark-submit TestScript.py