from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return 'Ok'


class Ticker(Resource):
    def get(self):
        # TODO
        return {
            'message': 'Ok'
        }


class Rates(Resource):
    def get(self):
        # TODO
        return {
            'message': 'Ok'
        }


api.add_resource(Ticker, '/ticker')
api.add_resource(Rates, '/rates')

if __name__ == '__main__':
    app.run(debug=True)
