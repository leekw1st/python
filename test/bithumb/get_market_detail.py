import pybithumb

detail = pybithumb.get_market_detail("BTC")

#시,고,저,종,거래량
print(detail)