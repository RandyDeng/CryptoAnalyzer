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


