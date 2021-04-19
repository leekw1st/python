"""
[전체 계좌 조회]
- 내가 보유한 자산 리스트를 보여줍니다
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

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}
jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/accounts", headers=headers)

print(res.json())

"""
currency	화폐를 의미하는 영문 대문자 코드	String
balance	주문가능 금액/수량	NumberString
locked	주문 중 묶여있는 금액/수량	NumberString
avg_buy_price	매수평균가	NumberString
avg_buy_price_modified	매수평균가 수정 여부	Boolean
unit_currency	평단가 기준 화폐	String]
"""