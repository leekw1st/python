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
    'currency': 'KRW',
    'state': 'processing',
}
query_string = urlencode(query)

txids = [
    'BKW-2021-05-04-c28f01e778af4d85671d893d14',
    #...
]
txids_query_string = '&'.join(["txids[]={}".format(txid) for txid in txids])

query['txids[]'] = txids
query_string = "{0}&{1}".format(query_string, txids_query_string).encode()

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

res = requests.get(server_url + "/v1/withdraws", params=query, headers=headers)

print(res.json())