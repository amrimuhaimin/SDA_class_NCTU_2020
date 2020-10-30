# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tLwpVuErgwWR3houJfsN9kwSRCZIf7yt
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time

#declare the website link
cmc = requests.get('https://coinmarketcap.com/')
soup = BeautifulSoup(cmc.content, 'html.parser')

#check the title format from the website
print(soup.title)

#the rest of format
print(soup.prettify())

data = soup.find('script', id="__NEXT_DATA__", type="application/json")
coins = {}
coins_data = json.loads(data.contents[0])
listings = coins_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
for i in listings:
  coins[str(i['id'])] = i['slug']

market_cap = []
volume = []
timestamp = []
name = []
symbol = []
slug = []
price = []
for i in coins:
  url = 'https://coinmarketcap.com/currencies/'+coins[i]+'/historical-data/?start=20200101&end=20201001'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  data = soup.find('script', id="__NEXT_DATA__", type="application/json")
  if not data:
    continue
  historical_data = json.loads(data.contents[0])
  quotes = historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]['quotes']
  info = historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]
  for j in quotes:
    timestamp.append(j['quote']['USD']['timestamp'])
    price.append(j['quote']['USD']['close'])
    market_cap.append(j['quote']['USD']['market_cap'])
    volume.append(j['quote']['USD']['volume'])
    name.append(info['name'])
    symbol.append(info['symbol'])
    slug.append(coins[i])
  
df = pd.DataFrame(columns=['timestamp', 'price', 'market_cap', 'volume', 'name', 'symbol', 'slug'])
df['price'] = price
df['market_cap'] = market_cap
df['volume'] = volume
df['timestamp'] = timestamp
df['name'] = name
df['symbol'] = symbol
df['slug'] = slug

#preprocess the timestamp
new_timestamp = []
for i in df['timestamp']:
  new_timestamp.append(i[:10])
df['timestamp'] = new_timestamp
df

df = df.pivot(index = "timestamp", columns="symbol", values=["price", "market_cap", "volume"])

df['market_cap'].to_csv('market.csv')
df['price'].to_csv('price.csv')
df['volume'].to_csv('volume.csv')
