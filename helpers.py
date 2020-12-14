import datetime
import requests
import os
import sqlite3
from time import sleep
import threading


def bitcoin_price_index_db():
    """
    Queries the database fetching all its data.
    :return: List of tuples containing date and price.
    """
    conn = sqlite3.connect('bitcoin.db')
    cursor = conn.cursor()

    return conn.execute('SELECT * FROM historical;').fetchall()


def bpi(date=datetime.date.today()):
    """
    Requests the CoinDesk's API for json file containing a bitcoin price index on specific dates.
    :param date: String or datetime object in format YYYY-MM-DD
    :return: A price_index dictionary if the request to the API goes right, None otherwise.
    """
    url = f'https://api.coindesk.com/v1/bpi/historical/close.json?start=2013-09-01&end={date}'

    # Contact API
    try:
        print(f'\tRequesting data from: {url}')
        response = requests.get(url)
        print('\tAPI connection: OK')

    except requests.RequestException:
        print(f"\tUnable to connect to the API")
        return None

    # Parse response
    try:
        quote = response.json()
        price_index = quote['bpi']
        return price_index

    except (KeyError, TypeError, ValueError):
        print("KeyError, TypeError, ValueError: couldn't parse response.")
        return None


def check_data(cursor):
    """
    Checks if the data in the database matches the API's.
    :param cursor: sqlite3 Cursor object.
    :return: True/False.
    """
    database_data = {item[0]: item[1] for item in cursor.execute('SELECT * FROM historical;').fetchall()}
    latest_database_date = list(database_data.keys())[-1]

    price_index = bpi(latest_database_date)

    if price_index == database_data:
        print('Database data: OK')
        return True

    else:
        print('Database data: NOT MATCHING')
        return False


def check_schema(cursor):
    """
    Checks if the schema of the database is not jeopardized.
    :param cursor: sqlite3 Cursor object
    :return: True/False
    """
    model = [(0, 'date', 'TEXT', 1, None, 0), (1, 'price', 'NUMERIC', 1, None, 0)]
    table_info = cursor.execute('PRAGMA table_info(historical);').fetchall()

    if table_info == model:
        print('Database schema: OK')
        return True

    else:
        print('Database schema: JEOPARDIZED')
        return False


def create_bitcoin_db():
    """Create the database and its cursor object to perform SQL commands"""
    conn = sqlite3.connect('bitcoin.db')
    c = conn.cursor()
    print('bitcoin.db was successfully created.')

    # Create table
    print('Creating table: CREATE TABLE historical (date TEXT NOT NULL, price NUMERIC NOT NULL);')

    c.execute('''CREATE TABLE historical (
        date TEXT NOT NULL,
        price NUMERIC NOT NULL
        );''')

    price_index = bpi()

    # Saving the data in bitcoin.db
    print("Saving the data in bitcoin.db")
    for key, value in price_index.items():
        c.execute('INSERT INTO historical (date, price) VALUES (?, ?);', (key, value))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print('bitcoin.db is set and up to date.')


def is_up_to_date(cursor):
    """
    Checks if data from database is up to date.
    :param cursor: sqlite3 Cursor object.
    :return: True/False.
    """
    database_data = {item[0]: item[1] for item in cursor.execute('SELECT * FROM historical;').fetchall()}
    latest_database_date = list(database_data.keys())[-1]

    price_index = bpi(latest_database_date)
    latest_bpi_date = list(price_index.keys())[-1]

    if latest_database_date == latest_bpi_date:
        print('Is the database up to date: YES')
        return True
    else:
        print('Is the database up to date: NO')
        return False


def price(code=''):
    """
    Request a json file from https://api.coindesk.com/v1/bpi/currentprice/<code>.json
    :param code: Currency symbol, like USD, BRL, etc
    :return: Current price
    """

    url = f'https://api.coindesk.com/v1/bpi/currentprice/{code}.json'

    # Contact API
    try:
        print(f'Requesting data from: {url}')
        response = requests.get(url)

    except requests.RequestException:
        print(f"RequestException: couldn't connect to: {url}.")
        return None

    # Parse response
    try:
        quote = response.json()
        rate = quote['bpi'][code]['rate_float']
        return f'${rate:,.2f}'

    except (KeyError, TypeError, ValueError):
        print("KeyError, TypeError, ValueError: couldn't parse response.")
        return None


def start_app(filename):
    """Terminal command to start a python script"""
    os.system(f'python3 {filename}')


def start_threads(target):
    """Starts the application threads"""
    files = ['database_manager.py', 'app.py']
    processes = []

    for file in files:
        processes.append(threading.Thread(target=target, args=(file,)))

    for process in processes:
        process.start()
        sleep(1)

