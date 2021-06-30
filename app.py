from flask import Flask, render_template
from helpers import Client

app = Flask(__name__)
client = Client()


@app.route('/')
def index():
    return render_template('index.html', data=client.get_crypto_data())


@app.route('/<string:cryptocurrency>')
def cryptocurrency(cryptocurrency):
    price = client.get_ticker(cryptocurrency)
    return f'{price}'


if __name__ == '__main__':
    app.run(debug=True)
