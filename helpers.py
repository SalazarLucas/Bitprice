import datetime
import requests


def bpi(start="2013-09-01", end=datetime.date.today()):
    """
    Requests the CoinDesk's API for json file containing a bitcoin price index on specific dates.
    :param start: String or datetime object in format YYYY-MM-DD
    :param end: String or datetime object in format YYYY-MM-DD
    :return: A price_index dictionary if the request to the API goes right, None otherwise.
    """

    url = f'https://api.coindesk.com/v1/bpi/historical/close.json?start={start}&end={end}'

    # Contact API
    try:
        response = requests.get(url)

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        price_index = quote['bpi']
        return price_index

    except (KeyError, TypeError, ValueError):
        return None


def current_price(code=''):
    """
    Request a json file from https://api.coindesk.com/v1/bpi/currentprice/<code>.json
    :param code: Currency symbol, like USD, BRL, etc
    :return: Current price
    """

    url = f'https://api.coindesk.com/v1/bpi/currentprice/{code}.json'

    # Contact API
    try:
        response = requests.get(url)

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        rate = quote['bpi'][code]['rate_float']
        return f'${rate:,.2f}'

    except (KeyError, TypeError, ValueError):
        return None
