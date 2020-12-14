import datetime
from helpers import check_data, check_schema, create_bitcoin_db, is_up_to_date, bpi
import os
import sqlite3
from time import sleep

try:
    while True:
        print('─' * 53 + 'API Status' + '─' * 52)
        # Verifies if the structure of the API data can be parsed by the application.
        if not bpi(datetime.date.today()):
            break

        # Ensures the database exists
        if not os.path.exists('bitcoin.db'):
            create_bitcoin_db()

        print('─' * 50 + 'Database Status' + '─' * 50)
        # Opening the database
        conn = sqlite3.connect('bitcoin.db')
        cursor = conn.cursor()

        # Ensures both database schema and data are correct.
        if not check_schema(cursor) or not check_data(cursor):
            os.remove("bitcoin.db")
            create_bitcoin_db()

        # Is up to date?
        if not is_up_to_date(cursor):
            pass

        conn.close()

        # Updates the database every hour
        print(f'Database updated at: {datetime.datetime.now()}')
        sleep(3600)

except KeyboardInterrupt:
    print('KeyboardInterrupt: application stopped.')
