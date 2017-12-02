from coinbase.wallet.client import Client
from coinbase.wallet.model import APIObject
from coinbasecredentials import COINBASE_KEY,COINBASE_SECRET_KEY
import time
import requests
import pprint
import datetime
client = Client(COINBASE_KEY, COINBASE_SECRET_KEY)
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')	
# obj = client._make_api_object(client._get('v2', 'prices', 'BTC-USD', 'historic'), APIObject)
# obj = client.get_currencies(currency_pair='BTC-USD')
# price = client.get_spot_price(currency_pair='ETH-USD', date='2014-05-10')

# print price
# print(client.get_spot_price(currency_pair='BTC-USD', date='2014-05-10'))
# print(client.get_spot_price(currency_pair='BTC-USD'))
# print(client.get_spot_price(currency_pair='BTC-USD', date='2014-11-30'))
# print(client.get_spot_price(currency_pair= 'BTC-USD', date=timestamp))
# pprint.pprint(requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot?date=2017-05-10").json())
# print timestamp

# currency_pair='BTC-USD'
# response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot").json()
# print(client.get_spot_price(currency_pair= 'BTC-USD'));
# print response;



response = requests.get("https://api.coindesk.com/v1/bpi/historical/close.json?start=2017-06-01&end=2017-12-01").json()
pprint.pprint(response)