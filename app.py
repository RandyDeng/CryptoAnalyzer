#!/usr/bin/env python
from flask import Flask, flash, jsonify, abort, request
from flask import render_template, redirect
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

import boto3
import time
import json
import requests

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

# Build query url for daily values
# inputs: start and end date in datetime format
def build_query_url(start, end):
	url = "https://api.coindesk.com/v1/bpi/historical/close.json?start="
	return url + start.strftime('%Y-%m-%d') + "&end=" + end.strftime('%Y-%m-%d')

# Main landing page
@app.route('/', methods=['GET'])
def index():
	#data = table.scan().get('Items')
	#print(data) # prints { 'Timestamp':'Timestamp_Test', 'Field1':'Field1_Test'}
	return render_template('home.html')

# Dashboard Showing Price
@app.route('/dashboard', methods=['GET'])
def dashboard():
	# build request query (probably not necessary)
	# start = datetime.strptime('2017-06-01', '%Y-%m-%d')
	# end = datetime.strptime('2017-07-01', '%Y-%m-%d')
	response = requests.get(build_query_url(start, end)).json()
	return render_template('dashboard.html')

# Analysis Tools
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
	if request.method == 'POST':
		# retrieve form information
		result = request.form
		running_avg = result.get('running_average')
		exponential_avg = result.get('exponential_average')
		momentum = result.get('momentum_line')
		# run analysis
	else:
		print("GET request sent")
	return render_template('charts.html')

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