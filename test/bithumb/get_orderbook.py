#################################################
#{
#'timestamp': '1618674303534',
#'payment_currency': 'KRW',
#'order_currency': 'BTC',
#'bids': [{'price': 77407000.0, 'quantity': 0.0259}, {'price': 77402000.0, 'quantity': 0.0297}, {'price': 77401000.0, 'quantity': 0.1766}, {'price': 77400000.0, 'quantity': 0.1486}, {'price': 77390000.0, 'quantity': 0.0015}], 
#'asks': [{'price': 77453000.0, 'quantity': 0.1034}, {'price': 77476000.0, 'quantity': 1.1}, 'price': 77479000.0, 'quantity': 0.079}, {'price': 77484000.0, 'quantity': 0.1459}, 'price': 77486000.0, 'quantity': 0.16676858}]
#}
#################################################

import pybithumb
import datetime

orderbook = pybithumb.get_orderbook("BTC")
ms = int(orderbook["timestamp"])

dt = datetime.datetime.fromtimestamp(ms/1000)

print(orderbook)    
print(dt)

bids = orderbook["bids"]    
asks = orderbook["asks"]    
print(bids)
print(asks)

for bid in bids:
    price = bid['price']   
    vol = bid['quantity']   
    print("매수호가:", price, "매도호가", vol)
    
