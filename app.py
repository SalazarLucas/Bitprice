from flask import Flask, render_template
from helpers import *

app = Flask(__name__)


@app.route('/')
def index():
    if update_database():
        return render_template("index.html",
                               price=price('USD'),
                               labels=[date[0] for date in bitcoin_price_index_db()],
                               values=[h_price[1] for h_price in bitcoin_price_index_db()])

    else:
        return render_template("api_problem.html")


if __name__ == "__main__":
    app.run()
