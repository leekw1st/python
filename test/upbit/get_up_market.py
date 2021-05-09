import pyupbit
import datetime
import time
import pprint


def get_up_market2():
    tickers = pyupbit.get_tickers("KRW")
    start_time = datetime.datetime.now()

    # 5일 이동평균 사용 상승장 대상 코인 
    # Input : tickers
    # Output : 5일 이동평균 사용하여 상승장으로 판단된 코인 색출
    i, j = 0, 100
    up_cnt, down_cnt= 0, 0
    len_all_list = len(tickers)

    while (j < len_all_list+100) :
        if(j>len_all_list) :
            j=len_all_list
        
        tickers_tmp = tickers[i:j]
        all_item = pyupbit.get_current_price(tickers_tmp)
        
        for ticker in all_item:
            df = pyupbit.get_ohlcv(ticker)
            ma5 = df['close'].rolling(5).mean()
            price = float(all_item[ticker])

            last_ma5 = ma5[-2]
            
            if price > last_ma5 : 
                print(ticker, "상승장")
                up_cnt=up_cnt+1
            else:
                print(ticker, '하락장')
                down_cnt=down_cnt+1
            
            time.sleep(0.03)
        
        i=i+100 
        j=j+100    

    end_time = datetime.datetime.now()

    print("상승:[",up_cnt,"]","하락:[",down_cnt,"]","소요시간:[",end_time - start_time, "]")


get_up_market2()