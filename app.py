#!/usr/bin/env python
from flask import Flask, flash, jsonify, abort, request
from flask import render_template, redirect
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta
from listener import bitcoin_listener
from pymongo import MongoClient
from subprocess import check_output

import boto3
import time
import json
import requests
import thread

app = Flask(__name__, static_url_path="")

# TODO IS AWS EVEN NECESSARY????
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

# Setup MongoDB
client = MongoClient()
db = client.FinalDB
collection = db.Aggregations

# Build query url for daily values
# inputs: start and end date in datetime format
def build_query_url(start, end):
	url = "https://api.coindesk.com/v1/bpi/historical/close.json?start="
	return url + start.strftime('%Y-%m-%d') + "&end=" + end.strftime('%Y-%m-%d')

# Convert formatted string into Linux Epcoh time
# timestamp is in datetime format '%Y-%m-%d %H:%M:%S'
def get_epoch(timestamp):
	pattern = '%Y-%m-%d %H:%M:%S'
	return int(time.mktime(time.strptime(timestamp, pattern)))

# Main landing page
@app.route('/', methods=['GET'])
def index():
	return render_template('home.html')

# Dashboard Showing Price
@app.route('/get_dashboard', methods=['GET'])
def get_dashboard():
	print("Info: Querying Coindesk for 24-hour bitcoin data")
	current_date = datetime.now()
	yesterday_date = datetime.now() - timedelta(days=30)
	response = requests.get(build_query_url(yesterday_date, current_date)).json()
	# TODO send data to front end...
	return jsonify(response)

# Dashboard Showing Price
@app.route('/dashboard', methods=['GET'])
def dashboard():
	print("Info: Querying Coindesk for 24-hour bitcoin data")
	current_date = datetime.now()
	yesterday_date = datetime.now() - timedelta(days=1)
	response = requests.get(build_query_url(yesterday_date, current_date)).json()
	# TODO send data to front end...
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
		# TODO send in appropriate inputs based on time and algorithm (how many datapoints???)
		current_date = datetime.now()
		yesterday_date = datetime.now() - timedelta(days=1)
		current_date = get_epoch(current_date.strftime('%Y-%m-%d %H:%M:%S'))
		yesterday_date = get_epoch(yesterday_date.strftime('%Y-%m-%d %H:%M:%S'))
		#temp = collection.find() # TODO read data from mongodb
		#for t in temp:
		#	print(t)
		print("Info: Begin spark analysis")
		check_output("/opt/spark/bin/spark-submit spark_script.py", shell=True)
		print("Info: Spark analysis complete")
		return render_template('charts.html', running_avg=[], exponential_avg=[], momentum=[]) # TODO populate with real data
	else:
		return render_template('charts.html', running_avg=[], exponential_avg=[], momentum=[])

# 500 Internal server error
@app.errorhandler(500)
def internal_server_error(e):
	return render_template("error_500.html"), 500

# 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
	return render_template("error_404.html"), 404

# Start data retrieval thread and server
if __name__ == '__main__':
	try:
		thread.start_new_thread(bitcoin_listener, ("bitcoin_listener", 2))
		print("Info: Starting bitcoin_listener thread")
	except:
		print("Error: unable to start thread")
	app.debug=True
	app.run(host='0.0.0.0', port=80)