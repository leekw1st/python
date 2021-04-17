import pybithumb 
import time

"""
while True:
    price = pybithumb.get_current_price("BTC") 
    print(price)

    time.sleep(1)
"""
tickers = pybithumb.get_tickers()

for tickers in tickers :
    price = pybithumb.get_current_price(tickers)
    print(tickers, price)
    time.sleep(0.1)