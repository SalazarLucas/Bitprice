from flask import Flask, render_template
from helpers import price, bitcoin_price_index_db

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html",
                           price=price('USD'),
                           labels=[date[0] for date in bitcoin_price_index_db()],
                           values=[h_price[1] for h_price in bitcoin_price_index_db()])


app.run()
