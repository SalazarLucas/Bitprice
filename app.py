from flask import Flask, render_template, jsonify
from helpers import currency_data, colors, spots

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", data=currency_data(), colors=colors())


if __name__ == "__main__":
    app.run()
