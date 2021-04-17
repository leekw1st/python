from pandas import DataFrame
import pandas as pd 
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

"""
data = { 'open':[100,200], 'high':[110,210]}
df = DataFrame(data)
print(df)
df = pd.read_excel("C:/Users/user/OneDrive/바탕 화면/test.xlsx")

df = df.set_index('date')

print(df)
"""

html = requests.get('https://finance.naver.com/item/frgn.nhn?code=005930&page=1') 

table = pd.read_html(html.text)