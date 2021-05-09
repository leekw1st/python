import pyupbit

# 종가 평균 계산
def get_moving_average(ticker, avg_day):
    btc = pyupbit.get_ohlcv(ticker)
    close = btc['close']
    ma = close.rolling(avg_day).mean()

    return ma

# 고가 평균 계산
def get_high_moving_average(ticker, avg_day):
    btc = pyupbit.get_ohlcv(ticker)
    high = btc['high']
    ma = high.rolling(avg_day).mean()

    return ma

# 저가 평균 계산
def get_low_moving_average(ticker, avg_day):
    btc = pyupbit.get_ohlcv(ticker)
    low = btc['low']
    ma = low.rolling(avg_day).mean()

    return ma


close = get_moving_average('KRW-DOGE', 1)    
print(close)
close = get_moving_average('KRW-DOGE', 5)    
print(close)