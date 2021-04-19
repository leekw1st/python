import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC")
print(df)

df2 = pyupbit.get_ohlcv("KRW-BTC", interval="minute1")
print(df2)