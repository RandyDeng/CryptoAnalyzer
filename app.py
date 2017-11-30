#!/usr/bin/env python
import flask
from flask import request, render_template, jsonify
import boto3
from boto3.dynamodb.conditions import Key, Attr
import cPickle as pickle
import datetime
import time
import json
import sys

app = Flask(__name__, static_url_path="")
app.secret_key = '{Uj@wtL=,E5NSWz#;&klzy8!czRoUdvE;rag|U3(dP$`E]eZ}fGVw)Y]-q#X=(>f'

#Enter AWS Credentials
aws_login = json.loads(open('aws.login').read())
AWS_ACCESS_KEY = aws_login['AWS_ACCESS_KEY']
AWS_SECRET_KEY = aws_login['AWS_SECRET_KEY']
REGION = aws_login['REGION']

# Get the table
dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY,
                            region_name=REGION)

table = dynamodb.Table('BitcoinResults')

@APP.route('/')
def index():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debut=True, host='0.0.0.0', port=80)
