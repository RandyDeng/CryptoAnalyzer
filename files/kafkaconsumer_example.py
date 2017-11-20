from random import randrange
import time
import datetime
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer

#Connect to Kafka 
client = KafkaClient("ip-10-179-181-24.ec2.internal:6667")
consumer = SimpleConsumer(client, "test-group", "topicname")

#Get messages from topic        
for message in consumer:
    print(message)
    print message.message.value
    



