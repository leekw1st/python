from pandas import Series

date = ['2021-01-01','2021-01-02','2021-01-03','2021-01-04','2021-01-05']
xrp_close = [100, 200, 300, 400, 500]
s = Series(xrp_close, index=date)
print(s)
