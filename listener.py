# Listener that retrieves data from bitcoin charts every 3 days

from datetime import datetime
from os import listdir, rename
from subprocess import check_output

import time
import urllib
import json

root = "bitcoin_history/"
update_file = "bitcoin.update"
bitcoin_file = "bitstampUSD.csv"
bitcoin_file_new = "bitstampUSD_NEW.csv"
zip_file = "bitstampUSD_NEW.csv.gz"

def update_timestamp(timestamp):
	file = open(root + update_file, 'w')
	file.write(timestamp)
	file.close()

def bitcoin_listener(thread_name, delay):
	while(True):
		ls = listdir(root)
		if not update_file in ls:
			update_timestamp('{"timestamp":"2000-1-1"}')
		timestamp = json.loads(open(root + update_file).read()).get('timestamp')
		last_updated = datetime.strptime(timestamp, '%Y-%m-%d')
		current_day = datetime.now()
		difference = (current_day - last_updated).days
		# retrieve/update data and timestamp
		if (difference >= 3) or (not bitcoin_file in ls):
			print("Info: Updating bitcoin historical data file")
			data = urllib.URLopener()
			data.retrieve("http://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz", root + zip_file)
			check_output("gunzip -f " + root + zip_file, shell=True)
			rename(root + bitcoin_file_new, root + bitcoin_file)
			update_timestamp('{"timestamp":"' + current_day.strftime('%Y-%m-%d') + '"}')
			print("Info: Bitcoin historical data finished updating")
		else:
			print("Info: No update necessary")
		# sleep for 1 day
		print("Info: Thread sleeping for 1 day")
		time.sleep(86400)