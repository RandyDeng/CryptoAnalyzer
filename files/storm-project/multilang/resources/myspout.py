from storm import Spout, emit, log
import time
import datetime
from random import randrange

            
def getData():	
	datalist=['38,54,8376,242',
	'38,13,15271,333',
	'26,98,3363,612',
	'38,51,7560,308',
	'42,36,6209,350',
	'12,32,13560,114',
	'58,59,3832,315',
	'33,9,13522,330',
	'49,24,2884,132']

	data = datalist[randrange(0,8)]
	return data

class MySpout(Spout):
    def nextTuple(self):
        time.sleep(2)
        data = getData()
        emit([data])

   
SensorSpout().run()
