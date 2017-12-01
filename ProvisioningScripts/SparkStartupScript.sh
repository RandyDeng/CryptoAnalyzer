#!/bin/bash
sudo apt update
sudo apt install openjdk-8-jdk -y
sudo apt install python -y
wget http://apache.claz.org/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz
sudo tar xzf spark-2.2.0-bin-hadoop2.7.tgz -C /opt
cd /opt
sudo ln -fs spark-2.2.0-bin-hadoop2.7 /opt/spark
cd ~/
sudo echo "export SPARK_HOME=/opt/spark
PATH=\$PATH:\$SPARK_HOME/bin
export PATH" >> .bashrc
source ./.bashrc
#Note- the source command doesn't inherently work in a bash script like this. You'll either have to log out and log back in the node, or run the source command yourself. 
