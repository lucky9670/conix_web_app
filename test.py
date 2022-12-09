# from forex_python.converter import CurrencyRates

# c = CurrencyRates()

# currency = c.get_rate( 'INR','USD')

# inr = float(input('Enter Indian Rupee : '))

# print(f'{inr} INR is eqaul to {round(inr*currency,2)} Doller')

# import requests

# class CurrencyRates():
#     url = 'https://api.exchangerate-api.com/v4/latest/USD'
    
#     def __init__(self):
#         self.data= requests.get(self.url).json()
#         self.currencies = self.data['rates']

#     def convert(self, from_currency, to_currency, amount): 
#         initial_amount = amount 
#         #first convert it into USD if it is not in USD.
#         # because our base currency is USD
#         if from_currency != 'USD' : 
#             amount = amount / self.currencies[from_currency] 
    
#         # limiting the precision to 4 decimal places 
#         amount = round(amount * self.currencies[to_currency], 2) 
#         return amount

        
# c = CurrencyRates()
# inr = int(input("Currency amount"))
# currency = c.convert('INR','USD', inr)


# print(currency)


# import requests
# url = "https://test.payu.in/merchant/postservice?form=2"
# payload = "key=&command=&var1=&var2=&var3=&var4=&var5=&var6=&var7=&var8=&var9=&hash="
# headers = { "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded" }
# response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
# print(response.text)


# importing Pandas module
import pandas as pd

# Creating a Function
def check_weekday(date):
	
	# computing the parameter date
	# with len function
	res=len(pd.bdate_range(date,date))
	
	if res == 0 :
		print("This is weekend")
	else:
		print("This is your working day")

# user input
date = "2020-08-17"
check_weekday(date)

date = "2020-08-16"
check_weekday(date)

