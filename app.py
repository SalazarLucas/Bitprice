from flask import Flask, render_template
from helpers import *

app = Flask(__name__)


@app.route('/')
def index():
    spot = spot_price('BTC-USD')
    last_day_rates = historic_rates('BTC-USD', '1D')
    last_five_days_rates = historic_rates('BTC-USD', '5D')
    last_month_rates = historic_rates('BTC-USD', '1M')

    if all([spot, last_day_rates]):
        return render_template("index.html",
                               spot=spot,
                               last_day_rates=last_day_rates,
                               last_five_days_rates=last_five_days_rates,
                               last_month_rates=last_month_rates)

    else:
        return render_template("api_problem.html")


if __name__ == "__main__":
    app.run()
