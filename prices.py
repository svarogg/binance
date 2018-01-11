from decimal import *

cache = {}

def update_cache(client):
    global cache
    cache = client.get_all_tickers()

def of(symbol):
    global cache
    return [Decimal(x['price']) for x in cache if x['symbol'] == symbol][0]
