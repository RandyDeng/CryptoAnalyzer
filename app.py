#!/usr/bin/env python
from flask import Flask, flash, jsonify, abort, request
from flask import render_template, redirect
from boto3.dynamodb.conditions import Key, Attr

import boto3
import time
import datetime
import json

app = Flask(__name__, static_url_path="")
app.secret_key = '{Uj@wtL=,E5NSWz#;&klzy8!czRoUdvE;rag|U3(dP$`E]eZ}fGVw)Y]-q#X=(>f'

#Enter AWS Credentials
aws_login = json.loads(open('login.key').read())
AWS_ACCESS_KEY = aws_login['AWS_ACCESS_KEY']
AWS_SECRET_KEY = aws_login['AWS_SECRET_KEY']
REGION = aws_login['REGION']

# Get the table
dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
							aws_secret_access_key=AWS_SECRET_KEY,
							region_name=REGION)

table = dynamodb.Table('BitcoinResults')

# Main landing page
@app.route('/', methods=['GET'])
def index():
	data = table.scan().get('Items')
	print(data) # prints { 'Timestamp':'Timestamp_Test', 'Field1':'Field1_Test'}
	return render_template('dashboard.html')

# 500 Internal server error
@app.errorhandler(500)
def internal_server_error(e):
	return render_template("Server error :("), 500

# 404 Not Found
@app.errorhandler(404)
def page_nots_found(e):
	return render_template("Page not found :("), 404

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)