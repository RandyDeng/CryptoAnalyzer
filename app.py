#!/usr/bin python
from flask import Flask, flash, jsonify, abort, request
from flask import render_template, redirect
from datetime import datetime, timedelta
from listener import bitcoin_listener, bitcoin_daily
from pymongo import MongoClient
from subprocess import check_output
from os import listdir

import time
import json
import requests
import thread

app = Flask(__name__, static_url_path="")

# Setup MongoDB
client = MongoClient()
db = client.FinalDB
collection = db.Aggregations

# Convert formatted string into Linux Epcoh time
# timestamp is in datetime format '%Y-%m-%d %H:%M:%S'
def get_epoch(timestamp):
	pattern = '%Y-%m-%d %H:%M:%S'
	return int(time.mktime(time.strptime(timestamp, pattern)))

# Main landing page
@app.route('/', methods=['GET'])
def index():
	return render_template('home.html')

# Returns json of daily data retrieved from bitcoin_daily thread
@app.route('/get_dashboard', methods=['GET'])
def get_dashboard():
	try:
		response = eval(open('bitcoin_history/bitcoin_daily.csv').read())
	except:
		print("Error: Could not read daily value from json")
	return jsonify(response)

# Returns json of Current Price used in dashboard.html to create live graph
@app.route('/get_currentprice', methods=['GET'])
def get_currentprice():
	response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
	response = {"bpi": response["bpi"]["USD"]["rate"]}
	return jsonify(response)

# Dashboard Showing Price
@app.route('/dashboard', methods=['GET'])
def dashboard():
	return render_template('dashboard.html')

# Analysis Tools
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
	if request.method == 'POST':
		# retrieve form information
		result = request.form
		time_period = result.get('time_period')
		start_date = result.get('start_date')
		try:
			start_date = get_epoch(start_date)
		except:
			print("Error: User input is not allowed")
			return render_template('charts.html', running_avg=[], exponential_avg=[], momentum=[])
		# retrieve data
		if time_period == 'hour':
			end = start_date + 3600
		if time_period == 'day':
			end = start_date + 86400
		if time_period == 'week':
			end = start_date + 604800
		if time_period == 'month':
			end = start_date + 2629743
		if time_period == 'year':
			end = start_date + 31556926
		# run analysis and retrieve data
		items = collection.find_one({'FromEpoch':start_date, 'ToEpoch':end})
		if items == None:
			print("Info: Begin spark analysis")
			try:
				check_output("/opt/spark-2.2.0-bin-hadoop2.7/bin/spark-submit --master local[*] --driver-memory 6g spark_script.py " + str(start_date), shell=True)
			except:
				print("Error: Spark has crashed while processing")
				return render_template('charts.html', running_avg=[], exponential_avg=[], momentum=[])
			print("Info: Spark analysis complete")
			return render_template('charts.html', running_avg=[], exponential_avg=[], momentum=[])
		print("Info: Grabbing data")
		items = collection.find_one({'FromEpoch':start_date, 'ToEpoch':end})
		a1 = items.get('RunningAverage')
		a2 = items.get('ExponentialAverage')
		a3 = items.get('MomentumLine')
		print("Info: Sending data to front-end")
		return render_template('charts.html', running_avg=a1, exponential_avg=a2, momentum=a3, start=start_date, end=end)
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
		thread.start_new_thread(bitcoin_daily, ("bitcoin_daily", 4))
		print("Info: Starting bitcoin_daily thread")
	except:
		print("Error: unable to start thread")
	app.run(debug=True, host='0.0.0.0', port=80)
