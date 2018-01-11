import init
import json
from pprint import pprint
import decimal

from init import client
import balances
import prices
import trades

decimal.getcontext().prec = 8

blacklisted = ['BCC', 'ETH', 'BTC']
bal = [x for x in balances.balances(client) if x['asset'] not in blacklisted]

prices.update_cache(client)

total_change_btc = 0

for b in bal:
    symbol = b['asset'] + 'BTC'
    got = b['total']
    avg_price = trades.avg_price(client, symbol)
    cur_price = prices.of(symbol)
    change = ((cur_price-avg_price)/avg_price) * 100
    got_btc = got * cur_price
    paid_btc = got * avg_price
    change_btc = got_btc - paid_btc

    total_change_btc += change_btc

    print(str(b['asset']) + ":")
    print("\tGot                : " + str(got))
    print("\tIn BTC             : " + str(got_btc))
    print("\tPaid BTC           : " + str(paid_btc))
    print("\tChange BTC         : " + str(change_btc))
    print("\tAvarage buy price  : " + str(avg_price))
    print("\tCurrent price      : " + str(cur_price))
    print("\tChange %:          : " + str(change))

print()
print("Total change btc : " + str(total_change_btc))
