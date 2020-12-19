from flask import Flask, render_template
from helpers import *

app = Flask(__name__)


@app.route('/')
def index():
    current = current_price('USD')
    price_index = bpi()

    if all([current, price_index]):
        return render_template("index.html",
                               price=current,
                               labels=[date for date in price_index.keys()],
                               values=[price for price in price_index.values()])

    else:
        return render_template("api_problem.html")


if __name__ == "__main__":
    app.run()
