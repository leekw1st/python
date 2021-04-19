import pyupbit

tickers = pyupbit.get_tickers()
print(tickers)
print(len(tickers))

tickers = pyupbit.get_tickers(fiat="KRW")
print(tickers)