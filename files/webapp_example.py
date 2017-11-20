from flask import Flask
import urllib2
import boto.dynamodb
app = Flask(__name__)
from datetime import date
today = date.today()

#-------Connect to DynamoDB---------
ACCESS_KEY="#"
SECRET_KEY="#"
REGION="us-east-1"

conn_db = boto.dynamodb.connect_to_region(REGION,
   aws_access_key_id=ACCESS_KEY,
   aws_secret_access_key=SECRET_KEY)

table = conn_db.get_table('tablename')
#-----------------------------------
   
@app.route('/')
def tweet_home():

    #Scan DynamoDB table
    results=table.scan()
    
    html = '<html><body><table width=80% border=1 align="center">'+\
            '<tr><td><strong>Timestamp</strong></td><td><strong>Date</strong></td><td><strong>Data</strong></td><td><strong>Prediction</strong></td></tr>'
            
    for result in results:
        html+='<td>'+result['data']+'</td><td>'+result['prediction']+'</td></tr>'


    html+='</table></body></html>'

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0')
