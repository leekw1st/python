import jwt          # PyJWT
import uuid
import hashlib
import pyupbit
import datetime
import time
import pprint
from urllib.parse import urlencode
from pyupbit.request_api import _send_get_request, _send_post_request, _send_delete_request, _call_public_api


def net_change_desc(tickers, coin_cnt):
    try:
        url = "https://api.upbit.com/v1/ticker"
        contents = _call_public_api(url, markets=tickers)[0]

        ret = {}       

        for content in contents:
            market = content['market']

            price = content['trade_price']
            open_price = content['opening_price']
            prev_closing_price = content['prev_closing_price']

            ret[market]['price'] = price
            ret[market]['open_price'] = open_price
            ret[market]['prev_closing_price'] = prev_closing_price
        return ret
    except Exception as x:
        print(x.__class__.__name__)

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
    print("ma",days,"_golden_cross Strategy START")

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
    print("ma",days,"_golden_cross Strategy END.")

    return coin

class Coinpot:
    def __init__(self, access, secret):
        self.access = access
        self.secret = secret

    def _request_headers(self, query=None):
        payload = {
            "access_key": self.access,
            "nonce": str(uuid.uuid4())
        }

        if query is not None:
            m = hashlib.sha512()
            m.update(urlencode(query).encode())
            query_hash = m.hexdigest()
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = "SHA512"

        #jwt_token = jwt.encode(payload, self.secret, algorithm="HS256").decode('utf-8')
        jwt_token = jwt.encode(payload, self.secret, algorithm="HS256")     # PyJWT >= 2.0
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorization_token}
        return headers


    # 계좌의 전체 상태를 조회
    def get_account_status(self):
        try:
            url = "https://api.upbit.com/v1/accounts"
            headers = self._request_headers()
            result = _send_get_request(url, headers=headers)
            asset_list = result[0]
            asset_list_length = len(asset_list)
            total_asset = 0
            total_buy_price = 0 
            total_current_price = 0

            for i in range(asset_list_length):
                currency = asset_list[i]['currency']
                balance = float(asset_list[i]['balance'])
                avg_buy_price = float(asset_list[i]['avg_buy_price'])

                if currency == 'KRW' :
                    print("보유원화:", currency, ", 평가금액 : ", balance)
                    total_asset = total_asset + balance
                else  :
                    price = pyupbit.get_current_price('KRW-' + currency)
                    print("보유코인:" ,currency,
                    ", 보유수량 : " , balance,
                    ", 평가금액 : " , price * balance,
                    ", 매수평균가 : " , avg_buy_price,
                    ", 매수금액 : ", balance * avg_buy_price,
                    ", 평가손익 : ",  price * balance - balance * avg_buy_price,
                                "[", round((price * balance - avg_buy_price * balance)/(avg_buy_price * balance) * 100, 2) ,"]")
                    total_asset = total_asset + price * balance
                    total_buy_price = total_buy_price + (avg_buy_price * balance)
                    total_current_price = total_current_price +  (price *balance)

            print("총 보유자산 : ", total_asset, 
                ", 총 매수금액 : ", total_buy_price,
                ", 총 평가금액 : ", total_current_price,
                ", 총 평가손익 : ", total_current_price - total_buy_price,
                "[",round((total_current_price - total_buy_price) / total_buy_price * 100, 2),"]")     
        except Exception as x:
            print(x.__class__.__name__)
            return None

    # 투자 가능한 금액 조회
    def get_invest_asset(self):
        try:
            invest_asset=0
            url = "https://api.upbit.com/v1/accounts"
            headers = self._request_headers()
            result = _send_get_request(url, headers=headers)
            asset_list = result[0]
            asset_list_length = len(asset_list)

            for i in range(asset_list_length):
                currency = asset_list[i]['currency']
                balance = float(asset_list[i]['balance'])
                #---------------------------------------
                # 보유 원화 조회
                # 투자가능 금액 결정 전략 추가
                #---------------------------------------
                if currency == 'KRW' :
                    # invest_asset = Strategy(balance)
                    invest_asset = balance * 0.7

            return invest_asset                    

        except Exception as x:
            print(x.__class__.__name__)
            return None


    def get_holding_coin_cnt(self):
        try:
            holding_coin_cnt=0
            url = "https://api.upbit.com/v1/accounts"
            headers = self._request_headers()
            result = _send_get_request(url, headers=headers)
            asset_list = result[0]
            holding_coin_cnt= len(asset_list)-1
            
            return holding_coin_cnt
        
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_coin_list(self, coin_cnt=1):
        try:
            tickers = pyupbit.get_tickers("KRW")
            start_time = datetime.datetime.now()
            
            #------------------------------------
            # Coin 검색 전략 추가
            #------------------------------------
            #tickers = ma_golden_cross(tickers, 60)
            #tickers = ma_golden_cross(tickers, 20)
            #tickers = ma_golden_cross(tickers, 5)

            tickers = net_change_desc(tickers, coin_cnt)
            
            end_time = datetime.datetime.now()
            print("대상코인수:[",len(tickers),"]","소요시간:[",end_time - start_time, "]")
            print("코인[",tickers,"]")
                    
        except Exception as x:
            print(x.__class__.__name__)
            return None



if __name__ == "__main__":
    import pprint
    with open("./key/upbit.txt") as f:
        lines = f.readlines()
        access = lines[0].strip()
        secret = lines[1].strip()

    # Coinpot Trading 사용을 위한 객체 생성
    coinpot = Coinpot(access, secret)

    # 해당 계좌의 상태 조회
    #coinpot.get_account_status()
    
    # 투자 가능 금액 조회
    #invest_asset = coinpot.get_invest_asset()
    
    # 보유 코인 갯수 조회
    #holding_coin_cnt = coinpot.get_holding_coin_cnt()
    
    # 투자 대상 코인 조회
    target_coin= coinpot.get_coin_list()

#    print("투자 가능 금액 :", invest_asset, "보유코인 갯수:", holding_coin_cnt)
    print("투자 대상 코인 :", target_coin)
    