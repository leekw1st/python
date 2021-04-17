import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/item/main.nhn?code=008560"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html5lib")
tags = soup.select("#chart_area > div.rate_info > div > p.no_today > em.no_down > span")
tag = tags[0]

print(tag.text)