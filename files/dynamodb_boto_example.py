import boto.dynamodb2
from boto.dynamodb2.table import Table
import time
from datetime import date
from awscredentials import ACCESS_KEY,SECRET_KEY,EC2_KEY_HANDLE

REGION="us-east-1"

print "Connecting to DynamoDB"

conn = boto.dynamodb2.connect_to_region(REGION,
   aws_access_key_id=ACCESS_KEY,
   aws_secret_access_key=SECRET_KEY)


print "Books description"

table=Table('books',connection=conn)
desc = table.describe()
print desc

print "Writing data"

item = table.put_item(data={
        'isbn':'9781494435143',
        'publishedDate':'2013-12-09',
        'Title': 'Cloud Computing: A Hands-on Approach',
        'Pages': 456,
        'Images':'''{"FrontCover":"http://cloudcomputingbook.info/images/frontcover.jpg",
                    "BackCover":"http://cloudcomputingbook.info/images/frontcover.jpg"}'''
    },overwrite=True)

print "Reading data"



read_data = table.get_item(isbn='9781494435143',publishedDate='2013-12-09')


print read_data.items()

all_items=table.scan()

for item in all_items:
    print item.items()


print "Done!"


