##############################################
# python for/while test
##############################################

coin = ["BTC", "ETH", "XRP", "BCH"]

for value in coin:
    print(value)

for num in [1,2,3,4,5,6,7,8,9,10]:
    print(num)

for num in range(1,21):
    print(num)

for num in range(1,21,2):
    print(num)

cur_price = {'BTC' : 10000, 'XRP' : 20000}

for ticker in cur_price:
    print(ticker)#  key 값이 출력

for ticker, price in cur_price.items():
    print(ticker, price)

for ticker in cur_price:
    print(ticker, cur_price[ticker])