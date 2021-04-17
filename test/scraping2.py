import requests
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup

context = ssl._create_unverified_context()
url = "https://finance.naver.com/item/main.nhn?code=008560"

html = urlopen(url,context=context)

soup = BeautifulSoup(html, "html5lib")
tags = soup.select("#chart_area > div.rate_info > div > p.no_today > em > span")

tag = tags[0]

print(tag.text)