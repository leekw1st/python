##############################################
# python list test
##############################################

coin = ['BTC','ETH','XRP','BCH']

print(coin)

coin.append("DASH")

print(coin)

coin.insert(1,'LKW')

print(coin)


price = [1,2,3,4,5,6,7,8,9,10]

print("max : " + str(max(price)))
print("min : " + str(min(price)))
print("avg : " + str(sum(price)/len(price)))