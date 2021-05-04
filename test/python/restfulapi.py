import requests
import datetime

coin_list=("currency_pair=btc_krw", "currency_pair=xrp_krw")

for coin in coin_list:
    url = "https://api.korbit.co.kr/v1/ticker/detailed?" + coin
    r = requests.get(url)

    bitcoin = r.json()

    timestamp = bitcoin['timestamp']

    date = datetime.datetime.fromtimestamp(timestamp/1000)

    print(date)