import pyupbit
import time

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

def ma_golden_cross(tickers, interval, term):
    i, j = 0, 100
    up_cnt, down_cnt= 0, 0
    len_all_list = len(tickers)
    coin = []

    while (j < len_all_list+100) :
        if(j>len_all_list) :
            j=len_all_list
        
        tickers_tmp = tickers[i:j]
        all_item = pyupbit.get_current_price(tickers_tmp)
        
        for ticker in all_item:
            df = pyupbit.get_ohlcv(ticker, interval)
            ma = df['close'].rolling(term).mean()
            price = float(all_item[ticker])

            last_ma = ma[-2]
            
            if price > last_ma : 
                up_cnt=up_cnt+1
                print(ticker, "상승장")
                coin.append(ticker)
            else:
                down_cnt=down_cnt+1
                print(ticker, "하락장")
            
            time.sleep(0.05)
        
        i=i+100 
        j=j+100    

    print("ma",interval,"_golden_cross Strategy. result[",up_cnt,"]")

    return coin


if __name__ == "__main__":
    tickers = pyupbit.get_tickers("KRW")
    
    #ticker = ma_golden_cross(tickers, 'days', 5) 
    tickers = ma_golden_cross(tickers, interval='day', term=3)
    print(tickers)
    tickers = ma_golden_cross(tickers, interval='minutes1', term=3)
    print(ticker)