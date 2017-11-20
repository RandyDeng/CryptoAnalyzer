from random import randrange
import time
import datetime
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer

#Connect to Kafka 
client = KafkaClient("ip-10-179-181-24.ec2.internal:6667")
producer = SimpleProducer(client)

#Send some synthetic data to Kafka topic
while True:
    ts=time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data = str(ts)  + ',' + str(timestamp)  + ',' + str(randrange(0,60))  + ',' + \
           str(randrange(0,100)) + ',' + str(randrange(5000,12000)) +  \
             ',' + str(randrange(0,100))
     
    print data        
    producer.send_messages('topicname', data)

    time.sleep(1)
    



