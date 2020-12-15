import datetime
import os
import requests
import sqlite3


def bitcoin_price_index_db():
    """
    Queries the database fetching all its data.
    :return: List of tuples containing date and price.
    """
    conn = sqlite3.connect('bitcoin.db')
    cursor = conn.cursor()

    return cursor.execute('SELECT * FROM historical;').fetchall()


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


def check_data(cursor):
    """
    Checks if the data in the database matches the API's.
    :param cursor: sqlite3 Cursor object.
    :return: True/False.
    """
    database_data = {item[0]: item[1] for item in cursor.execute('SELECT * FROM historical;').fetchall()}
    latest_database_date = list(database_data.keys())[-1]

    price_index = bpi(end=latest_database_date)

    if price_index == database_data:
        return True

    else:
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
        return True

    else:
        return False


def create_bitcoin_db():
    """Create the database and its cursor object to perform SQL commands"""
    conn = sqlite3.connect('bitcoin.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE historical (
        date TEXT NOT NULL,
        price NUMERIC NOT NULL
        );''')

    price_index = bpi()

    # Saving the data in bitcoin.db
    for key, value in price_index.items():
        c.execute('INSERT INTO historical (date, price) VALUES (?, ?);', (key, value))

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def is_up_to_date(cursor):
    """
    Checks if data from database is up to date.
    :param cursor: sqlite3 Cursor object.
    :return: True/False.
    """
    latest_database_date = cursor.execute("SELECT * FROM historical ORDER BY date DESC LIMIT 1;").fetchall()[0][0]
    latest_bpi_date = [i for i in bpi(start=latest_database_date).items() if i[0] != latest_database_date][-1][0]

    if latest_database_date == latest_bpi_date:
        return True
    else:
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


def update_database():
    # Verifies if the structure of the API data can be parsed by the application.
    if not bpi():
        return False

    # Ensures the database exists
    if not os.path.exists('bitcoin.db'):
        create_bitcoin_db()

    # Opening the database
    conn = sqlite3.connect('bitcoin.db')
    cursor = conn.cursor()

    # Ensures both database schema and data are correct.
    if not check_schema(cursor) or not check_data(cursor):
        os.remove("bitcoin.db")
        create_bitcoin_db()

    # Is up to date?
    if not is_up_to_date(cursor):
        latest_database_date = cursor.execute("SELECT * FROM historical ORDER BY date DESC LIMIT 1;").fetchall()[0][0]
        missing_price_index = [i for i in bpi(start=latest_database_date).items() if i[0] != latest_database_date]

        for date, price in missing_price_index:
            cursor.execute('INSERT INTO historical (date, price) VALUES (?, ?);', (date, price))

    conn.commit()
    conn.close()
    return True
