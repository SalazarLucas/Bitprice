from flask import Flask, render_template
from helpers import *

app = Flask(__name__)


@app.route('/')
def index():
    current = current_price('USD')
    dates = [date for date in bpi().keys()]
    prices = [price for price in bpi().values()]
    if all([current, dates, prices]):
        return render_template("index.html",
                               price=current,
                               labels=dates,
                               values=prices)

    else:
        return render_template("api_problem.html")


if __name__ == "__main__":
    app.run()
