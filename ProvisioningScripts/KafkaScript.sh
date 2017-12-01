#!/bin/bash
sudo apt update
sudo apt install openjdk-8-jdk -y
sudo apt install python -y
wget http://apache.claz.org/kafka/1.0.0/kafka_2.11-1.0.0.tgz
tar zxf kafka_2.11-1.0.0.tgz
mv kafka_2.11-1.0.0 kafka
cd kafka/
nohup bin/zookeeper-server-start.sh config/zookeeper.properties > ~/zookeeper-logs &
nohup bin/kafka-server-start.sh config/server.properties > ~/kafka-logs &

# http://www.bogotobogo.com/Hadoop/BigData_hadoop_Zookeeper_Kafka.php
# https://dzone.com/articles/installing-and-running-kafka-on-an-aws-instance
# Note- the default Kafka server will take up 1 gig of ram. If you're running this on a t2.micro instance, you need to run the following command as well:
# sed -i 's/-Xmx1G -Xms1G/-Xmx500m -Xms500m/' bin/kafka-server-start.sh
#note- the default kafka port is 9092, so you will need to open it on the AWS security group. 