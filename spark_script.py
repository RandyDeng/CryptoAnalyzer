import numpy as np
from pyspark import SparkContext
from pymongo import MongoClient
import sys
client = MongoClient()
db = client.FinalDB
collection = db.Aggregations
sc = SparkContext('local',"Simple App")
data = sc.textFile('./bitstampUSD.csv')
fromEpoch = int(sys.argv[1]) 
print(fromEpoch)
#1315922000
HourEpoch= fromEpoch + 3600
DayEpoch= fromEpoch + 86400
WeekEpoch= fromEpoch + 604800
MonthEpoch= fromEpoch + 2629743
print("Month:"+str(MonthEpoch) + " Week"+str(WeekEpoch)+" DayEpoch"+str(DayEpoch)+" HourEpoch"+str(HourEpoch)+"\n")
#1315922024
MonthFilteredRDD = data.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= MonthEpoch))
MonthFiltered = MonthFilteredRDD.collect()
print("Items in month:"+str(len(MonthFiltered))+"\n")
WeekFilteredRDD = MonthFilteredRDD.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= WeekEpoch))
WeekFiltered = WeekFilteredRDD.collect()
print("Items in week:"+str(len(WeekFiltered))+"\n")
DayFilteredRDD = WeekFilteredRDD.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= DayEpoch))
DayFiltered = DayFilteredRDD.collect()
print("Items in day:"+str(len(DayFiltered))+"\n")
HourFilteredRDD = DayFilteredRDD.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= HourEpoch))
HourFiltered = HourFilteredRDD.collect()
print("Items in hour:"+str(len(HourFiltered))+"\n")
FilteredSets=[MonthFiltered,WeekFiltered,DayFiltered,HourFiltered]
count=1
for Set in FilteredSets:
    PriceList=[]
    for x in Set:
        PriceList.append(float(str(x).split(",")[1]))
    RunningAverage = np.convolve(PriceList, np.ones((2,))/2, mode='valid')
    if(count==1):
        toEpoch=MonthEpoch
        N=3000
    elif(count==2):
        toEpoch=WeekEpoch
        N=1500
    elif(count==3):
        toEpoch=DayEpoch
        N=300
    elif(count==4):
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
        counter=counter+1
    post = {"FromEpoch": fromEpoch,
             "ToEpoch": toEpoch,
             "RunningAverage": list(RunningAverage),
             "ExponentialAverage": list(ExponentialAverage),
             "MomentumLine": list(moments)}
    print(post)
    collection.insert_one(post)
    count=count+1

#submit this script with spark-submit TestScript.py