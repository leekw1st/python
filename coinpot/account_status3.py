"""
내 계좌 상태
"""
import pyupbit
import pprint
import datetime

with open("./key/upbit.txt") as f:
    lines = f.readlines()
    access = lines[0].strip()
    secret = lines[1].strip()

#Exchange API 사용을 위한 객체 생성
upbit = pyupbit.exchange_api.Upbit(access, secret)

asset_list = upbit.get_balances()
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
    