
import pyupbit
import datetime
import time
import pprint


#-----------------------------------------------
# N일 이동평균선 상향 돌파 코인 탐색
# Input
#   tickers : 검색대상 coin
#   days : N일
#-----------------------------------------------
def ma_golden_cross(tickers, days):
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
            df = pyupbit.get_ohlcv(ticker)
            ma = df['close'].rolling(days).mean()
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

    #pprint.pprint(coin)
    return coin

def search_coin():
    #------------------------------------------------------
    # - 모든 코인 중 원하는 전략의 코인을 탐색
    # - 각 전략 함수
    #   --> Input Type = List
    #   --> Output Type = List    
    #   --> Input 과 Output은 'tickers'로 통일
    # - 소요시간 : 대상 코인을 찾는데 소요된 시간
    # - 대상코인수 : 추가된 전략 대상 코인의 갯수
    #-----------------------------------------------------
    tickers = pyupbit.get_tickers("KRW")
    start_time = datetime.datetime.now()

    #------------------------------------
    # Coin 검색 전략 추가
    #------------------------------------
    tickers = ma_golden_cross(tickers, 60)

    #------------------------------------
    # Strtegy End.
    #------------------------------------
    
    end_time = datetime.datetime.now()
    print("대상코인수:[",len(tickers),"]","소요시간:[",end_time - start_time, "]")
    print("코인[",tickers,"]")


if __name__ == "__main__":
    search_coin()