import storm
from datetime import date
import time
import datetime
import boto.dynamodb

ACCESS_KEY="###"
SECRET_KEY="###"
REGION="us-east-1"

today = date.today()

#Connect to DynamoDB
conn_db = boto.dynamodb.connect_to_region(REGION,
   aws_access_key_id=ACCESS_KEY,
   aws_secret_access_key=SECRET_KEY)
   

def analyzeData(data):
    #Add your code for data analysis here
    return True

class MyBolt(storm.BasicBolt):
    def process(self, tup):
        data = tup.values[0]

        output = analyzeData(data)
        
        result= "Result: "+ str(output)

        #Store analyzed results in DynamoDB
        table = conn_db.get_table("tablename")
        item_data = {
            'data':str(data),
            'prediction':str(output),
        }

        item = table.new_item(
        hash_key=str(today),
        range_key=str(data),
        attrs=item_data
        )
        item.put()
                            
        storm.emit([result])


SensorBolt().run()


