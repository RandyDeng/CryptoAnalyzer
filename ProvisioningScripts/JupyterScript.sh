#!/bin/bash
sudo apt update
sudo apt install openjdk-8-jdk -y
sudo apt install python -y
sudo apt install python-pip -y
sudo pip install -U pip setuptools
sudo pip install jupyter


# https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook
# to utilize jupyter, ssh with -L 8888:127.0.0.1:8888 and you can copy the link they give you and it will work. 