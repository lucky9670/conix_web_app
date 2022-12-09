import requests

class CurrencyRates():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'

    def __init__(self):
        self.data= requests.get(self.url).json()
        self.currencies = self.data['rates']

    def get_rate(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        #first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
    
        # limiting the precision to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 2) 
        return amount

