import pyupbit

orderbook = pyupbit.get_orderbook("KRW-DOGE")

test = orderbook.json()

print(test)