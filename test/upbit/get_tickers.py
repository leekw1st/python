import pyupbit

tickers = pyupbit.get_tickers()
print(tickers)

tickers = pyupbit.get_tickers(fiat="KRW")
print(len(tickers))