import requests


class Client:
    def __init__(self):
        self.__base_url = 'https://api.pro.coinbase.com'

    def get_ticker(self, id):
        # Requests the API
        ticker = self.__base_url + f'/products/{id}-USD/ticker'
        request = requests.get(ticker)

        # Parse response
        response = request.json()
        price = response['price']

        return price

    def __get_currencies(self):
        # Requests the API
        currencies = self.__base_url + '/currencies'
        request = requests.get(currencies)

        # Parse response
        response = request.json()
        
        return response

    def __get_products(self):
        # Requests the API
        products = self.__base_url + '/products'
        request = requests.get(products)

        # Parse response
        response = request.json()
        products_list = [p['base_currency'] for p in response if p['quote_currency'] == 'USD']
        products_list.sort()

        return products_list

    def get_crypto_data(self):
        products = self.__get_products()
        currencies = self.__get_currencies()
        data = list()

        for product in products:
            for currency in currencies:
                if product == currency['id']:
                    crypto_data = {
                        'id': product,
                        'name': currency['name']
                    }
                    data.append(crypto_data)
                    break
        
        return data


#client = Client()

#print(client.get_ticker('BTC'))