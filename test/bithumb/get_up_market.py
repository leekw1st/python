import pybithumb
import datetime

def get_up_market():
    tickers = pybithumb.get_tickers()
    start_time = datetime.datetime.now()

    for ticker in tickers :
        df = pybithumb.get_ohlcv(ticker)
        ma5 = df['close'].rolling(5).mean()
        
        price = pybithumb.get_current_price(ticker)

        last_ma5 = ma5[-2]

        if price > last_ma5 : 
            print(ticker, "상승장")
        else:
            print(ticker, '하락장')

    end_time = datetime.datetime.now()

    print("소요시간:[",end_time - start_time, "]")

def get_up_market2():
    all = pybithumb.get_current_price("ALL")
    start_time = datetime.datetime.now()

    up_cnt = 0
    down_cnt = 0

    for ticker, data in all.items():
        df = pybithumb.get_ohlcv(ticker)
        ma5 = df['close'].rolling(5).mean()
        price = float(data['closing_price'])

        last_ma5 = ma5[-2]
        
        if price > last_ma5 : 
            print(ticker, "상승장")
            up_cnt=up_cnt+1
        else:
            print(ticker, '하락장')
            down_cnt=down_cnt+1
        
    end_time = datetime.datetime.now()

    print("상승:[",up_cnt,"]","하락:[",down_cnt,"]","소요시간:[",end_time - start_time, "]")

get_up_market2()