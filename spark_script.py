import numpy as np
from pyspark import SparkContext
from pymongo import MongoClient
import math
import sys

client = MongoClient()
db = client.FinalDB
collection = db.Aggregations

sc = SparkContext('local',"Simple App")
data = sc.textFile('bitcoin_history/bitstampUSD.csv')
fromEpoch = int(sys.argv[1])

#print(fromEpoch)
#1315922000
HourEpoch= fromEpoch + 3600
DayEpoch= fromEpoch + 86400
WeekEpoch= fromEpoch + 604800
MonthEpoch= fromEpoch + 2629743
YearEpoch= fromEpoch + 31556926
#print("Month:"+str(MonthEpoch) + " Week"+str(WeekEpoch)+" DayEpoch"+str(DayEpoch)+" HourEpoch"+str(HourEpoch)+"\n")
#1315922024
YearFilteredRDD = data.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= YearEpoch))
YearFiltered = YearFilteredRDD.collect()
MonthFiltered = sc.parallelize(YearFiltered).filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= MonthEpoch)).collect()
#print("Items in month:"+str(len(MonthFiltered))+"\n")
WeekFiltered = sc.parallelize(MonthFiltered).filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= WeekEpoch)).collect()
#print("Items in week:"+str(len(WeekFiltered))+"\n")
DayFiltered = sc.parallelize(WeekFiltered).filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= DayEpoch)).collect()
#print("Items in day:"+str(len(DayFiltered))+"\n")
HourFiltered = sc.parallelize(DayFiltered).filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= HourEpoch)).collect()
#print("Items in hour:"+str(len(HourFiltered))+"\n")

FilteredSets=[YearFiltered,MonthFiltered,WeekFiltered,DayFiltered,HourFiltered]
count=0
for Set in FilteredSets:
    PriceList=[]
    legnth=len(Set)
    if(legnth>1000):
        filternumber=0
        filterlist=np.linspace(0,len(Set),1000,dtype=int)

        for x in Set:
            if(filternumber in filterlist):
                PriceList.append(float(str(x).split(",")[1]))
            filternumber=filternumber+1
    else:
        for x in Set:
            PriceList.append(float(str(x).split(",")[1]))
    RunningAverage = np.convolve(PriceList, np.ones((2,))/2, mode='valid')
    N=int(round(math.sqrt(len(PriceList))/2)+1)
    if(count==0):
        toEpoch=YearEpoch
    elif(count==1):
        toEpoch=MonthEpoch
    elif(count==2):
        toEpoch=WeekEpoch
    elif(count==3):
        toEpoch=DayEpoch
    elif(count==4):
        toEpoch=HourEpoch
    RunningAverage = np.convolve(PriceList, np.ones((N,))/N, mode='valid')
    weights = np.exp(np.linspace(-1, 0, N))
    ExponentialAverage = np.convolve(PriceList, weights / weights.sum(), mode='valid')[:len(PriceList)]
    ExponentialAverage[:N] = ExponentialAverage[N]
    moments = np.zeros((len(PriceList) - 1,))
    counter = 0
    last_data = 0
    for current_data in PriceList:
        if counter < 2:
            moments[count - 1] = (current_data - last_data) * 0.75
        elif counter >= 2:
            moments[counter - 1] = moments[counter - 2] + (current_data - last_data) * 0.75
        last_data = current_data
        counter = counter + 1
    post = {"FromEpoch": fromEpoch,
             "ToEpoch": toEpoch,
             "RunningAverage": list(RunningAverage),
             "ExponentialAverage": list(ExponentialAverage),
             "DataPoints":len(PriceList),
             "MomentumLine": list(moments)
            }
    #print(post)
    # path = '/home/ubuntu/CryptoAnalyzer/analysis_output/'+str(fromEpoch)+"_"+str(toEpoch)+".bdat"
    # actualpost={"FromEpoch": fromEpoch,
    #          "ToEpoch": toEpoch,
    #          "Location": path,
    #          "DataPoints":len(PriceList)
    #         }
    collection.insert_one(post)
    #outputfile = open(path,'w')
    #outputfile.write(str(post))
    #outputfile.close()
    count=count+1

#submit this script with spark-submit TestScript.py
