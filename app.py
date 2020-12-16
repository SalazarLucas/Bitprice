from flask import Flask, render_template
from helpers import *

app = Flask(__name__)


@app.route('/')
def index():
    update = update_database()
    current = current_price('USD')
    if update and current:
        return render_template("index.html",
                               price=current,
                               labels=[date[0] for date in bitcoin_price_index_db()],
                               values=[price[1] for price in bitcoin_price_index_db()])

    else:
        return render_template("api_problem.html")


if __name__ == "__main__":
    app.run()
