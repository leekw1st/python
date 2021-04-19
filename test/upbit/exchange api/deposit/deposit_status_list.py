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
}
query_string = urlencode(query)

txids = [
    'BKD-2021-05-02-7c6e02715da3e1f85d29d966d9',
    'BKD-2021-05-02-b17ce7e69bb35e6f921b256038',
    'BKD-2021-05-02-ad08a2c8f438798b403667daf0',
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

res = requests.get(server_url + "/v1/deposits", params=query, headers=headers)

print(res.json())