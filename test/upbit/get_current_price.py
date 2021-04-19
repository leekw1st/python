import pyupbit

price1 = pyupbit.get_current_price("KRW-XRP")

price2 = pyupbit.get_current_price("KRW-BTC")

price3 = pyupbit.get_current_price("BTC-XRP")

price = pyupbit.get_current_price(["BTC-XRP", "KRW-XRP"])


tickers = pyupbit.get_tickers()

price = pyupbit.get_current_price(tickers)
print(price)