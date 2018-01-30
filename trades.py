from pprint import pprint
from decimal import *


def create_closed_deal(top, total_buy, total_sell, paid, got):
    return {
        'top': top,
        'paid': paid,
        'got': got,
        'avg_buy': paid / total_buy,
        'avg_sell': got / total_sell
    }


def create_open_deal(total_buy, total_sell, paid):
    return {
        'balance': total_buy - total_sell,
        'paid': paid,
        'avg_price': paid / total_buy
    }


def scan(client, asset, symbol):
    print(symbol)
    trades = client.get_my_trades(symbol=symbol)

    total_buy = Decimal(0)
    total_sell = Decimal(0)
    top = Decimal(0)
    paid = Decimal(0)
    got = Decimal(0)
    closed_deals = []
    open_deal = None
    for trade in trades:
        qty = Decimal(trade['qty'])
        price = Decimal(trade['price'])

        if trade['isBuyer']:
            paid += qty * price
            total_buy += qty
            if trade['commissionAsset'] == asset:
                total_buy -= Decimal(trade['commission'])

            if total_buy > top:
                top = total_buy
        else:
            got += qty * price
            total_sell += qty
            if trade['commissionAsset'] == 'BTC':
                got -= Decimal(trade['commission'])

            if total_buy - total_sell < 1:
                if total_buy > 0:
                    closed_deals.append(create_closed_deal(top, total_buy, total_sell, paid, got))
                top = Decimal(0)

    if total_buy - total_sell > 1:
        open_deal = create_open_deal(total_buy, total_sell, paid)
    return {
        'asset': asset,
        'closed': closed_deals,
        'open': open_deal
    }
