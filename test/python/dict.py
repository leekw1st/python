##############################################
# python dict test
##############################################

coin = {'BTC':100,'ETH':200,'XRP':300,'BCH':400}

print(coin)

print(list(coin.keys()))
print(list(coin.values()))

coin['LKW']=999
print(coin)

result = {'error': {'message': '일시적인 거래량 급증으로 먼저 접수된 주문을 처리중입니다. 잠시 후 주문을 시도해 주세요.', 'name': 'too_many_request_order'}}

#if list(result.keys())[0] == 'error':
#    print("hello")

#if 'LK' not in coin.keys():    
#    print("hello")
if 'error' in result.keys():    
    print("hello")