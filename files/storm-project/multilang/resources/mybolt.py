import storm

class MyBolt(storm.BasicBolt):
    def process(self, tup):
        data = tup.values[0].split(',')

	result= "Predicted: "+ str(data)

	storm.emit([result])


SensorBolt().run()
