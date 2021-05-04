import pandas as pd
import requests
import ssl
import urllib.request 
from bs4 import BeautifulSoup
from pandas import DataFrame
"""
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
url = "https://finance.naver.com/item/sise_day.nhn?code=008560"

req = urllib.request.Request(url, headers = headers); 

context = ssl._create_unverified_context()

html = urllib.request.urlopen(req, context=context)

soup = BeautifulSoup(html, "lxml")

html_table = soup.select("table")

print(len(html_table))

table = pd.read_html(str(html_table))

print(table)
"""
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
url = "https://finance.naver.com/item/sise_day.nhn?code=008560"

req = urllib.request.Request(url, headers = headers); 

html = urllib.request.urlopen(req)

soup = BeautifulSoup(html, "lxml")

html_table = soup.select("table")

table = pd.read_html(str(html_table))

#print(table[0].dropna(axis=0))
df = DataFrame(table,index=data)
#print(table[0].dropna(axis=0).index)
print(df)



