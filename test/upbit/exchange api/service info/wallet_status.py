"""
입출금 현황
- 입출금 현황 및 블록 상태를 조회
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

res = requests.get(server_url + "/v1/status/wallet", headers=headers)

print(res.json())

"""
필드	설명	타입
currency	화폐를 의미하는 영문 대문자 코드	String
wallet_state	입출금 상태
- working : 입출금 가능
- withdraw_only : 출금만 가능
- deposit_only : 입금만 가능
- paused : 입출금 중단
- unsupported : 입출금 미지원	String
block_state	블록 상태
- normal : 정상
- delayed : 지연
- inactive : 비활성 (점검 등)	String
block_height	블록 높이	Integer
block_updated_at	블록 갱신 시각	DateString
"""