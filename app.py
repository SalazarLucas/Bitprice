from flask import Flask, render_template
from helpers import *

app = Flask(__name__)


@app.route('/')
def index():
    spot = spot_price('BTC-USD')
    last_day_rates = historic_rates('BTC-USD', '1D')
    last_five_days_rates = historic_rates('BTC-USD', '5D')
    maximum = historic_rates('BTC-USD', 'MAX')

    if all([spot, last_day_rates]):
        return render_template("index.html",
                               spot=spot,
                               last_day_rates=last_day_rates,
                               last_five_days_rates=last_five_days_rates,
                               last_month_rates=maximum[-31::1],
                               last_year_rates=maximum[-365::1],
                               last_five_year_rates=maximum[-1825::1],
                               max_rates=maximum)

    else:
        return render_template("api_problem.html")


if __name__ == "__main__":
    app.run()
