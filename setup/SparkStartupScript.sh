#!/bin/bash
sudo apt update
sudo apt install openjdk-8-jdk -y
sudo apt install python -y
sudo apt install python-numpy -y
sudo apt install python-pip -y
sudo apt install mongodb -y
sudo apt install python-pymongo -y
sudo pip install -U pip setuptools
wget http://apache.claz.org/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz
sudo tar xzf spark-2.2.0-bin-hadoop2.7.tgz -C /opt
cd /opt
sudo ln -fs spark-2.2.0-bin-hadoop2.7 /opt/spark
cd /opt/spark
sudo cp conf/log4j.properties.template conf/log4j.properties
sudo sed -i 's/rootCategory=INFO/rootCategory=WARN/' conf/log4j.properties
cd ~/
sudo echo "export SPARK_HOME=/opt/spark
PATH=\$PATH:\$SPARK_HOME/bin
export PATH" >> .bashrc
source ./.bashrc
cd setup
mongo < MongoCommands.js
#Note- the source command doesn't inherently work in a bash script like this. You'll either have to log out and log back in the node, or run the source command yourself. 
#partially adapted from https://sparkour.urizone.net/recipes/installing-ec2/ 

# for someone who wants to do spark mlib via jupyter https://www.datacamp.com/community/tutorials/apache-spark-tutorial-machine-learning
