import jwt          # PyJWT
import uuid
import hashlib
import pyupbit
import datetime
import time
import pprint
import traceback
from urllib.parse import urlencode
from pyupbit.quotation_api import get_current_price
from pyupbit.request_api import _send_get_request, _send_post_request, _send_delete_request, _call_public_api

def _DEBUG_LOG_(function, log):
    time = datetime.datetime.now()
    date=time.strftime('%Y-%m-%d')
    time=time.strftime('%H:%M:%S')

    print('[',date,' ',time,']','[',function,']','[',log,']', sep='')

    dir = 'C:\\Source\\python\\coinpot\\log\\coinpot.log_'+date

    f = open(dir, "a", encoding='utf8')

    log = '['+date+' '+time+']'+'['+function+']'+'['+log+']'+'\n'
    
    f.write(log)

def net_change_desc(tickers, coin_cnt):
    try:
        url = "https://api.upbit.com/v1/ticker"
        contents = _call_public_api(url, markets=tickers)[0]
        coin_list = [] 
        
        for content in contents:
            coin = {}       
            market = content['market']

            price = content['trade_price']
            open_price = content['opening_price']
            prev_closing_price = content['prev_closing_price']

            coin['market'] = market
            coin['price'] = price
            coin['open_price'] = open_price
            coin['prev_closing_price'] = prev_closing_price
            coin['net_change'] = price - prev_closing_price
            coin_list.append(coin) 

        sorted_coin_list = sorted( coin_list, key=( lambda x : x['net_change']),reverse=True )

        return sorted_coin_list

    except Exception as x:
        print(traceback.format_exc())
        print(x.__class__.__name__)

#-----------------------------------------------
# N일 이동평균선 상향 돌파 코인 탐색
# Input
#   tickers : 검색대상 coin
#   days : N일
#-----------------------------------------------
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
                #print(ticker, "상승장")
                coin.append(ticker)
            else:
                down_cnt=down_cnt+1
                #print(ticker, "하락장")
            
            time.sleep(0.05)
        
        i=i+100 
        j=j+100    

    log = "ma_"+str(interval)+str(term)+"_golden_cross Strategy. result:"+str(up_cnt)
    _DEBUG_LOG_('ma_golden_cross()', log)

    return coin


class Coinpot:

    order_list = []

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
            total_coin_price = 0

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
                    total_coin_price = total_coin_price +  (price *balance)

            print("총 보유자산 : ", total_asset, 
                ", 총 매수금액 : ", total_buy_price,
                ", 총 평가금액 : ", total_coin_price,
                ", 총 평가손익 : ", total_coin_price - total_buy_price,
                "[",round((total_coin_price - total_buy_price) / total_buy_price * 100, 2),"]")     
        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None

    def get_balance(self):
        try:
            url = "https://api.upbit.com/v1/accounts"
            headers = self._request_headers()
            result = _send_get_request(url, headers=headers)
            return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None

    # 투자 가능한 금액 조회
    def get_invest_asset(self, invest_ratio=70):
        try:
            total_asset=0           #총자산
            total_invest_asset=0    #투자가능총자산
            total_coin_asset=0      #코인총자산
            locked_asset=0          #미체결총자산
            current_invest_asset=0  #현재투자가능자산

            balance_list = self.get_balance()
            
            for x in balance_list:
                currency = x['currency']
                balance = float(x['balance'])
                locked = round(float(x['locked']))
                
                if currency == 'KRW' :
                    locked_asset = locked_asset + locked
                    total_asset = round(total_asset + balance + locked_asset)
                else  :
                    price = pyupbit.get_current_price('KRW-' + currency)
                    locked_asset = locked_asset + (price * locked)
                    total_asset = round(total_asset + locked_asset + price * balance)
                    total_coin_asset = round(total_coin_asset + (price * balance))


            total_invest_asset = round((total_asset) * invest_ratio / 100) # 투자가능총자산
            
            current_invest_asset = round(total_invest_asset - total_coin_asset -locked_asset)
            
            log = "총자산:"+str(total_asset)+",원화:"+str(total_asset-total_coin_asset-locked_asset)+\
                  ",코인:"+str(total_coin_asset)+",투자가능총자산:"+str(total_invest_asset)+\
                  ",미체결:"+str( locked_asset)+",현재투자가능금액:"+str(current_invest_asset)
            
            _DEBUG_LOG_("get_invest_asset()", log)

            return current_invest_asset 

        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None


    def get_holding_coin_cnt(self):
        try:
            holding_coin_cnt=0
            url = "https://api.upbit.com/v1/accounts"
            headers = self._request_headers()
            result = _send_get_request(url, headers=headers)
            asset_list = result[0]
            holding_coin_cnt= len(asset_list)-1

            log = "보유코인갯수:"+str(holding_coin_cnt)

            _DEBUG_LOG_("get_holding_coin_cnt()", log)

            return holding_coin_cnt
        
        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None

    def coin_search(self, coin_cnt=1):
        try:
            while True:
                _DEBUG_LOG_("coin_search()","Coin Search Start!!")

                tickers = pyupbit.get_tickers("KRW")
                start_time = datetime.datetime.now()
                
                #------------------------------------
                # Coin 검색 전략 추가
                #------------------------------------
                #tickers = ma_golden_cross(tickers, interval='day', term=60)
                #tickers = ma_golden_cross(tickers, interval='day', term=20)
                tickers = ma_golden_cross(tickers, interval='day', term=3)
                #tickers = ma_golden_cross(tickers, interval='minutes1', term=5)
                tickers = ma_golden_cross(tickers, interval='minutes1', term=3)
                tickers = ma_golden_cross(tickers, interval='minutes1', term=1)

                if tickers:
                    tickers = net_change_desc(tickers, coin_cnt)

                end_time = datetime.datetime.now()

                if tickers:
                    break
            
            log = "소요시간:"+str(end_time - start_time)+"전략 대상 코인 수:"+str(len(tickers))
            _DEBUG_LOG_("coin_search()", log)

            return tickers

        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None

    
    def order_buy(self, ticker, investing_amount):
        """
        지정가 매수
        :param ticker: 마켓 티커
        :param price: 주문 가격
        :param volume: 주문 수량
        :return:
        """
        try:
            ticker_price = get_current_price(ticker)

            volume = investing_amount // ticker_price

            log = "대상:"+str(ticker)+",수량:"+str(volume)+",현재가:"+ str(ticker_price)+",투자금액:"+str(investing_amount)
            _DEBUG_LOG_("order_buy()", log)

            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,
                    "side": "bid",
                    "volume": str(volume),
                    "price": str(ticker_price),
                    "ord_type": "limit"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            
            return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None            

    def is_order_possible(self, ticker, investing_amount):
        try:
            ticker_price = get_current_price(ticker)

            volume = investing_amount // ticker_price

            if volume * ticker_price > 5000:
                return True 
            else:
                return False
        
        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None            

    def get_coin_count(self, ticker):
        try:
            url = "https://api.upbit.com/v1/accounts"
            headers = self._request_headers()
            result = _send_get_request(url, headers=headers)
            asset_list = result[0]
            asset_list_length = len(asset_list)

            for i in range(asset_list_length):
                currency = asset_list[i]['currency']

                if 'KRW-'+currency == ticker :
                    balance = float(asset_list[i]['balance'])
                    return balance

        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None


    def order_sell(self, ticker):
        try:
            _DEBUG_LOG_("order_sell()", "Sell~!!")
            
            ticker_price = get_current_price(ticker)
            volume = self.get_coin_count(ticker)

            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,
                    "side": "ask",
                    "volume": str(volume),
                    "price": str(ticker_price),
                    "ord_type": "limit"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)

            return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None

    def status_check(self, ticker):
        try:
            url = "https://api.upbit.com/v1/accounts"
            headers = self._request_headers()
            result = _send_get_request(url, headers=headers)
            asset_list = result[0]
            asset_list_length = len(asset_list)

            if  asset_list_length  > 0 :
                for x in asset_list:
                    currency = x['currency']
                    coin = 'KRW-'+x['currency']
                    balance = float(x['balance'])
                    avg_buy_price = float(x['avg_buy_price'])
                    
                    if coin == ticker and ticker != 'KRW':
                        price = pyupbit.get_current_price('KRW-' + currency)
                        rate = round((price * balance - avg_buy_price * balance)/(avg_buy_price * balance) * 100, 2)

                        if rate > 3:
                            signal = 'upsell'
                        elif rate < -2:
                            signal = 'downsell'
                        else:
                            signal = 'hold'

                        log="코인:"+str(coin)+", 수익률:"+str(rate)+", 주문신호:"+signal
                        _DEBUG_LOG_("status_check()", log)
                        
                        return signal

            return 'Not Exist'

        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None   

    def get_order_state(self, ticker, uuid):
        # TODO : states, uuids, identifiers 관련 기능 추가 필요
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {'market': ticker,
                    'state': 'wait',
                    'uuid': uuid,
                    'order_by': 'desc'
                    }
            headers = self._request_headers(data)
            result = _send_get_request(url, headers=headers, data=data)
            
            if result[0] :
                tmp_time = result[0][0]['created_at'][0:10] + ' ' + result[0][0]['created_at'][11:19]
                time_term = datetime.datetime.now() - datetime.datetime.strptime(tmp_time, '%Y-%m-%d %H:%M:%S')
                time_term_sec = time_term.seconds%60
                if time_term_sec > 3:
                    return 'cancel'
                else:
                    return 'wait'

            elif not result[0] :
                data = {'market': ticker,
                        'state': 'done',
                        'uuid': uuid,
                        'order_by': 'desc'
                        }
                headers = self._request_headers(data)
                result = _send_get_request(url, headers=headers, data=data)

            return result[0][0]['state']

        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
            return None

    def cancel_wait_order(self, uuid):
        try:
            url = "https://api.upbit.com/v1/order"
            data = {"uuid": uuid}
            headers = self._request_headers(data)
            result = _send_delete_request(url, headers=headers, data=data)

            return result[0]
        
        except Exception as x:
            print(x.__class__.__name__)
            print(traceback.format_exc())
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
    
    while True :  
        signal = 'default' 
        
        _DEBUG_LOG_("main()", "=====================================================================================================")
        
        # 보유 코인 갯수 조회
        holding_coin_cnt = coinpot.get_holding_coin_cnt()
        if holding_coin_cnt == 0:
            # 투자 가능 금액 조회
            current_invest_asset = coinpot.get_invest_asset(70)
            # 보유 코인 갯수와 최소 투자 가능 금액 조건이 만족할시 매수
            if current_invest_asset > 5000 :
                # 투자 대상 코인 조회
                target_coin= coinpot.coin_search()
                if len(target_coin) > 0 :
                    order_result = coinpot.order_buy(target_coin[0]['market'], current_invest_asset)    
                    if 'market' in order_result.keys():
                        print('UUID:', order_result['uuid'], '상태:', order_result['state'])

        if 'market' in order_result.keys():
            if coinpot.get_order_state(order_result['market'], order_result['uuid']) == 'done':
                signal = coinpot.status_check(order_result['market'])
                if signal == 'upsell' or signal == 'downsell' :
                    order_result = coinpot.order_sell(order_result['market']) 
                    print("매도주문:",order_result['uuid'], order_result['market'], order_result['state'])
            elif coinpot.get_order_state(order_result['market'], order_result['uuid']) == 'wait': 
                print('주문상태:',order_result['market'], 'waiting!!')        
            elif coinpot.get_order_state(order_result['market'], order_result['uuid']) == 'cancel':
                print("미체결주문취소:",coinpot.cancel_wait_order(order_result['uuid']))
        elif 'error' in order_result.keys():
            print("Error Check")

        time.sleep(1)    