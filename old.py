from datetime import datetime, timedelta
import requests
import sys


def spot_price(currency_pair='USD'):
    """
    Request the spot price from Coinbase API for a given currency pair.
    :param currency_pair: Crypto/fiat currencies pair (All crypto - USD pairs is set by default).
    :return: List of dictionaries with id, name and spot price for one or more cryptocurrencies.
    """

    url = f'https://api.coinbase.com/v2/prices/{currency_pair}/spot'
    cryptocurrencies = currency_names()
    cryptos = {}

    # Contact API
    try:
        response = requests.get(url)

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()['data']

        for key, value in cryptocurrencies.items():
            for spot in quote:
                #rates = historic_rates(key + '-USD')
                if key == spot['base']:
                    cryptos[key] = value
                    cryptos[key]['amount'] = f'{float(spot["amount"]):.2f}'
                    cryptos[key]['rates'] = historic_rates(key + '-USD')
                    break

        return cryptos

    except (KeyError, TypeError, ValueError):
        return None


def historic_rates(currency_pair):
    """
    Request the historic rates data from Coinbase API for a given currency pair in the last 30 days.
    :param currency_pair: Crypto/fiat currencies pair.
    :return: Two-dimensional matrix [ time, low, high, open, close, volume ].
    """
    url = f'https://api.pro.coinbase.com/products/{currency_pair}/candles'
    now = datetime.now()

    maximum = []

    # for request in range(requests_number):
    params = {'start': (now - timedelta(days=30)).strftime('%Y-%m-%d'),
              'end': now.strftime('%Y-%m-%d'),
              'granularity': 86400}

    # Contact API
    try:
        response = requests.get(url, params=params)

    except requests.RequestException:
        return None

    # Parse Response
    rates = response.json()
    try:
        for rate in reversed(rates):
            maximum.append(rate)

    except KeyError:
        print(f"{rates}", file=sys.stderr)

    return maximum


def currency_names():
    """Return id and name for all cryptocurrencies from Coinbase"""

    url = 'https://api.pro.coinbase.com/currencies'

    # Contact API
    try:
        response = requests.get(url)

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        quote = {cur['id']: {'name': cur['name']} for cur in quote if cur['details']['type'] == 'crypto'}
        return quote

    except (KeyError, TypeError, ValueError):
        return None


print(currency_names())
