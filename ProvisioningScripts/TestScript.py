import numpy as np
from pyspark import SparkContext
sc = SparkContext('local',"Simple App")
data = sc.textFile('./bitstampUSD.csv')

Filtered = data.filter(lambda x: (int(str(x).split(",")[0]) >= 1315922016 and int(str(x).split(",")[0]) <= 1315922024))
FilteredList=Filtered.collect()
PriceList=[]
for x in FilteredList:
    PriceList.append(float(str(x).split(",")[1]))
print(np.convolve(PriceList, np.ones((2,))/2, mode='valid'))

#submit this script with spark-submit TestScript.py