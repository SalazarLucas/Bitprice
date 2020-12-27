from datetime import datetime, timedelta
import requests


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
    :param key: 1D, 5D, 1M, 1Y, 5Y, MAX (1 Day, 5 Days, 1 Month...).
    :return: Two-dimensional matrix [ time, low, high, open, close, volume ].
    """
    url = f'https://api.pro.coinbase.com/products/{currency_pair}/candles'
    now = datetime.now()

    keys = {'1D': {'days_ago': 1,
                   'granularity': 300},  # 300 second intervals (5 min)
            '5D': {'days_ago': 5,
                   'granularity': 3600},
            '1M': {'days_ago': 31,
                   'granularity': 86400},
            '1Y': {'days_ago': 365,
                   'granularity': 86400},
            '5Y': {'days_ago': 1825,
                   'granularity': 86400},
            'MAX': {'days_ago': (now - datetime.strptime('2015-07-19', '%Y-%m-%d')).days,
                    'granularity': 86400}}

    params = {'start': (now - timedelta(days=keys[key]['days_ago'])).strftime('%Y-%m-%d %H:%M:%S'),
              'end': now.strftime('%Y-%m-%d %H:%M:%S'),
              'granularity': keys[key]['granularity']}

    # Contact API
    try:
        response = requests.get(url, params=params)

    except requests.RequestException:
        return None

    rates = response.json()
    return rates
