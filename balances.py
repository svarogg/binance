from decimal import *

def balances(client):
    data = client.get_account()['balances']

    balances = {}
    decimals = [{
        'asset':x['asset'],
        'free':Decimal(x['free']),
        'locked': Decimal(x['locked']),
        'total': Decimal(x['free']) + Decimal(x['locked'])}
            for x in data if Decimal(x['free']) > 0 or Decimal(x['locked']) > 0]
    filtered = [ x for x in decimals if x['total'] > 1]

    return sorted(filtered, reverse=True, key=lambda x: x['total'])
