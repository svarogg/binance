import json
from pprint import pprint
from decimal import *
import sys
import os

from init import client
import balances
import prices
import trades

getcontext().prec = 8

blacklisted = ['BCC', 'ETH', 'BTC', 'BNB']
bal = [x for x in balances.balances(client) if x['asset'] not in blacklisted]

if os.path.isfile('assets.json'):
    assets = json.load(open('assets.json'))
    for asset in assets:
        if len([x for x in bal if x['asset'] == asset]) == 0:
            bal.append({
                'asset': asset,
                'free': Decimal(0),
                'locked': Decimal(0),
                'total': Decimal(0)})

prices.update_cache(client)
all_deals = []
for b in bal:
    asset = b['asset']
    if(asset == 'USDT'):
        continue
    symbol = asset + 'BTC'
    all_deals.append(trades.scan(client, asset, symbol))


def open_trades():
    total_change_btc = 0
    open_deals = [x for x in all_deals if x['open'] != None]

    for deal in open_deals:
        symbol = deal['asset'] + 'BTC'
        have = deal['open']['balance']
        avg_price = deal['open']['avg_price']
        cur_price = prices.of(symbol)
        change = ((cur_price - avg_price) / avg_price) * 100
        have_btc = have * cur_price
        paid_btc = have * avg_price
        change_btc = have_btc - paid_btc

        target_10 = avg_price * 110 / 100
        target_20 = avg_price * 120 / 100
        target_30 = avg_price * 130 / 100

        total_change_btc += change_btc

        print(deal['asset'] + ":")
        print("\tHave               : " + str(have))
        print("\tIn BTC             : " + str(have_btc))
        print("\tChange BTC         : " + str(change_btc))
        print("\tAvarage buy price  : " + str(avg_price))
        print("\tCurrent price      : " + str(cur_price))
        print("\tChange %:          : " + str(change))
        print()
        print("\tTargets:")
        print("\t\t10% : " + str(target_10))
        print("\t\t20% : " + str(target_20))
        print("\t\t30% : " + str(target_30))

    print()
    print("Total change btc : " + str(total_change_btc))


def closed_trades():
    deals = [x for x in all_deals if len(x['closed']) > 0]
    total_btc = Decimal(0)

    for single_asset in deals:
        print(single_asset['asset'] + ":")
        symbol = single_asset['asset'] + 'BTC'
        for i, deal in enumerate(single_asset['closed']):
            amount = deal['top']
            buy_price = deal['avg_buy']
            sell_price = deal['avg_sell']
            paid = deal['paid']
            got = deal['got']
            bottom_line = got - paid
            percentage = bottom_line / paid * 100

            total_btc += bottom_line

            print("\tDeal No. " + str(i + 1))
            print("\t\tAmount          : " + str(amount))
            print("\t\tBuy Price       : " + str(buy_price))
            print("\t\tSell Price      : " + str(sell_price))
            print("\t\tPaid BTC        : " + str(paid))
            print("\t\tGot BTC         : " + str(got))
            print("\t\tBottom Line BTC : " + str(bottom_line))
            print("\t\tBottom Line %   : " + str(percentage))

    print()
    print("Total in BTC: " + str(total_btc))


verb = sys.argv[1]

options = {
        'open' : open_trades,
        'closed': closed_trades
        }

options[verb]()
