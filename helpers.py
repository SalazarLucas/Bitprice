import requests
import datetime
import json

NOW = datetime.datetime.now()
START = (NOW - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
END = NOW.strftime('%Y-%m-%d')


def spots(base='', currency='USD'):
    if base:
        base = base + '-'

    url = f"https://api.coinbase.com/v2/prices/{base}{currency}/spot"

    # Contact endpoint
    try:
        response = requests.get(url)
    
    except requests.RequestException:
        return None
    
    # Parse response
    try:
        spot = response.json()['data']
    
    except (KeyError, ValueError, TypeError):
        return None
    
    return spot


def rates(base, currency='USD', start=START, end=END, granularity=86400):
    url = f'https://api.pro.coinbase.com/products/{base}-{currency}/candles'
    params = {
        'start': start,
        'end': end,
        'granularity': granularity
    }
    
    # Contact endpoint
    try:
        response = requests.get(url, params=params)
    
    except requests.RequestException:
        return None
    
    # Parse response
    try:
        rates = response.json()
        rates.sort(reverse=False)
    
    except AttributeError:
        return None

    return [[rate[0], rate[2]] for rate in rates]


def currency_names(currency=''):
    """Return id and name for all cryptocurrencies from Coinbase"""
    url = f'https://api.pro.coinbase.com/currencies/{currency}'

    # Contact API
    try:
        response = requests.get(url)

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        quote = {cur['id']: {'name': cur['name']} for cur in quote if cur['details']['type'] == 'crypto'}

    except (KeyError, TypeError, ValueError):
        return None
    
    return quote


def currency_data():
    data = {}
    names = currency_names()

    for spot in spots():
        symbol = spot['base']
        rate = rates(symbol)

        if rate != None:
            name = names[symbol]['name']
            amount = f'{float(spot["amount"]):.2f}'

            with open('colors.json', 'r') as file:
                colors = json.load(file)

            try:
                data[symbol] = {
                    'name': name,
                    'amount': amount,
                    'color': colors[symbol],
                    'rates': rate
                }
            
            except KeyError:
                    data[symbol] = {
                    'name': name,
                    'amount': amount,
                    'color': "#202020",
                    'rates': rate
                }
    
    return data


def colors():
    with open('colors.json', 'r') as file:
        data = json.load(file)
    
    return data
