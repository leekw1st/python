"""
계좌 상태
1. 보유 KRW
2. 보유 자산
3. 평가 금액 및 수익률 등.
currency	화폐를 의미하는 영문 대문자 코드	String
balance	주문가능 금액/수량	NumberString
locked	주문 중 묶여있는 금액/수량	NumberString
avg_buy_price	매수평균가	NumberString
avg_buy_price_modified	매수평균가 수정 여부	Boolean
unit_currency	평단가 기준 화폐	String]
"""
import os
import jwt
import uuid
import hashlib
import requests
import pyupbit
from urllib.parse import urlencode

access_key = '6KJxPmeR58U1UpZyJcn8GMBKyxZ8fOx5UgDoyfED'
secret_key = 'ApD12Hxdryx0FhX2Gdc2l5Dh9n8N29uomgFboDhl'
server_url = 'https://api.upbit.com'

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}
jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/accounts", headers=headers)

asset_list = res.json()
asset_list_length = len(asset_list)
total_asset = 0
total_buy_price = 0 
total_current_price = 0

for i in range(asset_list_length):
    if asset_list[i]['currency'] == 'KRW' :
        print("보유원화:",asset_list[i]['currency'],", 평가금액 : " , asset_list[i]['balance'])
        total_asset = total_asset + float(asset_list[i]['balance'])
    else  :
        price = pyupbit.get_current_price(asset_list[i]['unit_currency'] + '-' + asset_list[i]['currency'])
        print("보유코인:" ,asset_list[i]['currency'],
        ", 보유수량 : " , asset_list[i]['balance'],
        ", 평가금액 : " , price * float(asset_list[i]['balance']),
        ", 매수평균가 : " , float(asset_list[i]['avg_buy_price']),
        ", 매수금액 : ", float(asset_list[i]['balance']) * float(asset_list[i]['avg_buy_price']),
        ", 평가손익 : ",  price * float(asset_list[i]['balance']) - float(asset_list[i]['balance']) * float(asset_list[i]['avg_buy_price']),
                     "[", round((price * float(asset_list[i]['balance']) - float(asset_list[i]['balance']) * float(asset_list[i]['avg_buy_price']))/
                             (float(asset_list[i]['balance']) * float(asset_list[i]['avg_buy_price'])) * 100, 2) ,"]")
        total_asset = total_asset + price * float(asset_list[i]['balance'])
        total_buy_price = total_buy_price + (float(asset_list[i]['avg_buy_price']) * float(asset_list[i]['balance']))
        total_current_price = total_current_price +  (price * float(asset_list[i]['balance']))

print("총 보유자산 : ", total_asset, 
    ", 총 매수금액 : ", total_buy_price,
    ", 총 평가금액 : ", total_current_price,
    ", 총 평가손익 : ", total_current_price - total_buy_price,
    "[",round((total_current_price - total_buy_price) / total_buy_price * 100, 2),"]") 