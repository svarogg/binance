from pprint import pprint
from decimal import *

def avg_price(client, pair):
    trades = client.get_my_trades(symbol = pair)

    total = Decimal(0)
    price = Decimal(0)
    for trade in trades:
        if trade['isBuyer']:

            qty = Decimal(trade['qty'])
            p = Decimal(trade['price'])

            price = (price * total + p * qty ) / (qty + total)
            total += qty
        else:
            total -= Decimal(trade['price'])

    return price
