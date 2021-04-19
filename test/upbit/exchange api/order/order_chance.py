"""
[주문가능정보]
- 마켓별 주문 가능 정보를 확인한다.
"""
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

#access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
#secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
#server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

access_key = '6KJxPmeR58U1UpZyJcn8GMBKyxZ8fOx5UgDoyfED'
secret_key = 'ApD12Hxdryx0FhX2Gdc2l5Dh9n8N29uomgFboDhl'
server_url = 'https://api.upbit.com'

query = {
    'market': 'KRW-XRP',
}
query_string = urlencode(query).encode()

m = hashlib.sha512()
m.update(query_string)
query_hash = m.hexdigest()

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)

print(res.json())


"""
bid_fee	매수 수수료 비율	NumberString
ask_fee	매도 수수료 비율	NumberString
market	마켓에 대한 정보	Object
market.id	마켓의 유일 키	String
market.name	마켓 이름	String
market.order_types	지원 주문 방식	Array[String]
market.order_sides	지원 주문 종류	Array[String]
market.bid	매수 시 제약사항	Object
market.bid.currency	화폐를 의미하는 영문 대문자 코드	String
market.bit.price_unit	주문금액 단위	String
market.bid.min_total	최소 매도/매수 금액	Number
market.ask	매도 시 제약사항	Object
market.ask.currency	화폐를 의미하는 영문 대문자 코드	String
market.ask.price_unit	주문금액 단위	String
market.ask.min_total	최소 매도/매수 금액	Number
market.max_total	최대 매도/매수 금액	NumberString
market.state	마켓 운영 상태	String
bid_account	매수 시 사용하는 화폐의 계좌 상태	Object
bid_account.currency	화폐를 의미하는 영문 대문자 코드	String
bid_account.balance	주문가능 금액/수량	NumberString
bid_account.locked	주문 중 묶여있는 금액/수량	NumberString
bid_account.avg_buy_price	매수평균가	NumberString
bid_account.avg_buy_price_modified	매수평균가 수정 여부	Boolean
bid_account.unit_currency	평단가 기준 화폐	String
ask_account	매도 시 사용하는 화폐의 계좌 상태	Object
ask_account.currency	화폐를 의미하는 영문 대문자 코드	String
ask_account.balance	주문가능 금액/수량	NumberString
ask_account.locked	주문 중 묶여있는 금액/수량	NumberString
ask_account.avg_buy_price	매수평균가	NumberString
ask_account.avg_buy_price_modified	매수평균가 수정 여부	Boolean
ask_account.unit_currency	평단가 기준 화폐	String
"""