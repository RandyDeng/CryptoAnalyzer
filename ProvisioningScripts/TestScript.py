import numpy as np
from pyspark import SparkContext
from pymongo import MongoClient

client = MongoClient()
db = client.FinalDB
collection = db.Aggregations
sc = SparkContext('local',"Simple App")
data = sc.textFile('./bitstampUSD.csv')
fromEpoch=1315922016
toEpoch=1315922024
Filtered = data.filter(lambda x: (int(str(x).split(",")[0]) >= fromEpoch and int(str(x).split(",")[0]) <= toEpoch))
FilteredList=Filtered.collect()
PriceList=[]
for x in FilteredList:
    PriceList.append(float(str(x).split(",")[1]))
result=np.convolve(PriceList, np.ones((2,))/2, mode='valid')
print(result)
post = {"FromEpoch": fromEpoch,
         "ToEpoch": toEpoch,
         "RunningAverage": list(result),
         "ExponentialAverage": ["0", "0", "0"],
         "MomentumLine": 0}
collection.insert_one(post)

#submit this script with spark-submit TestScript.py