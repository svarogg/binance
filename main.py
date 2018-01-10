from binance.client import Client
import json

from pprint import pprint

config = json.load(open('config.json'))

client = Client(config["key"], config["secret"])

pprint(client.get_order_book(symbol='BNBBTC'))
