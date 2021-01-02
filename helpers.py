from datetime import datetime, timedelta
from time import sleep
import requests
import sys


def spot_price(currency_pair='BTC-USD'):
    """
    Request the spot price from Coinbase API for a given currency pair.
    :param currency_pair: Crypto/fiat currencies pair.
    :return: Spot price
    """

    url = f'https://api.coinbase.com/v2/prices/{currency_pair}/spot'

    # Contact API
    try:
        response = requests.get(url)

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        spot = quote['data']['amount']
        return f'${spot}'

    except (KeyError, TypeError, ValueError):
        return None


def historic_rates(currency_pair, key):
    """
    Request the historic rates data from Coinbase API for a given currency pair.
    :param currency_pair: Crypto/fiat currencies pair.
    :param key: 1D, 5D, MAX (1 Day, 5 Days, MAX).
    :return: Two-dimensional matrix [ time, low, high, open, close, volume ].
    """
    url = f'https://api.pro.coinbase.com/products/{currency_pair}/candles'
    now = datetime.now()

    keys = {'1D': {'days_ago': 1,
                   'granularity': 300},  # 300 second intervals (5 min)
            '5D': {'days_ago': 5,
                   'granularity': 3600},
            'MAX': {'days_ago': (now - datetime.strptime('2015-07-19', '%Y-%m-%d')).days,
                    'granularity': 86400}}

    if key in ['1D', '5D']:
        params = {'start': (now - timedelta(days=keys[key]['days_ago'])).strftime('%Y-%m-%d %H:%M:%S'),
                  'end': now.strftime('%Y-%m-%d %H:%M:%S'),
                  'granularity': keys[key]['granularity']}

        # Contact API
        try:
            response = requests.get(url, params=params)
            sleep(0.25)

        except requests.RequestException:
            return None

        rates = list(reversed(response.json()))

        return rates

    # Coinbase API returns maximum 300 aggregations per request for historical data.
    # In order to get yearly data, with 86400 granularity seconds, it is needed to do multiple requests.
    elif key == 'MAX':
        maximum = []
        requests_number = round(keys['MAX']['days_ago'] / 300)
        start = datetime.strptime('2015-07-19', '%Y-%m-%d')

        for request in range(requests_number):
            params = {'start': start.strftime('%Y-%m-%d'),
                      'end': (start + timedelta(days=300)).strftime('%Y-%m-%d'),
                      'granularity': 86400}

            # Contact API
            try:
                response = requests.get(url, params=params)
                sleep(0.25)

            except requests.RequestException:
                return None

            # Parse Response
            rates = response.json()
            try:
                for rate in reversed(rates):
                    maximum.append(rate)

                start = datetime.utcfromtimestamp(rates[0][0]) + timedelta(days=1)

            except KeyError:
                print(f"{rates}", file=sys.stderr)
                print(f"{request}", file=sys.stderr)

        return maximum
