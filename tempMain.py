from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import pandas as pd
import json

database_file = 'database.csv'
 
try:
    database = pd.read_csv(database_file)
    print('case 1')
except ValueError:
    database = pd.DataFrame(columns=['Date', 'Item', 'AveragePrice'])
    print('case 2')

items = database['Item'].unique().tolist()
print('ITEMS: ' + str(items))
print('DATABASE LOADED: ' + str(database))

master_frame = pd.DataFrame(columns=items)
print(master_frame)

with open('tracked-links.json', 'r') as f:
    trackedLinks = json.loads(f.read())

def getPricesByLink(link: str) -> list: # Returns list of prices scraped from a given ebay link
    r = requests.get(link)
    pageParse = BeautifulSoup(r.text, "html.parser")
    searchResults = pageParse.find('ul', {'class': 'srp-results'}).find_all("li", {'class': 's-item'})
    
    itemPrices = []
    
    for result in searchResults:
        priceAsText = result.find('span', {'class': 's-item__price'}).text
        if 'to' in priceAsText:
            continue
        price = float(priceAsText[3:].replace(',', ''))  
        itemPrices.append(price)
    return itemPrices

def removeOutliers(prices: list, m=2) -> list:
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def getAverage(prices: list) -> float:
    return np.mean(prices)

for item in trackedLinks.keys():
    print(item)
    prices = getPricesByLink(trackedLinks[item])
    listings = pd.Series(removeOutliers(prices))
    listings.sort_values(kind='mergesort', ignore_index=True)  
    maximum = listings.max()
    minimum = listings.min()
    averagePrice = getAverage(listings)
    new_row_df = pd.DataFrame([{'Date': datetime.now(), 'Item': item, 'AveragePrice': averagePrice}])
    database = pd.concat([database, new_row_df], ignore_index=True)
    master_frame[item] = listings
    print(master_frame)
print(database)

plt.figure(figsize=(10, 6))  

for item in database['Item'].unique():
    item_df = database[database['Item'] == item]

    plt.plot([datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f') for date in item_df['Date']], item_df['AveragePrice'], label=item)

# Format the x-axis with dates
date_formatter = mdates.DateFormatter('%Y-%m-%d')
plt.gca().xaxis.set_major_formatter(date_formatter)
plt.gcf().autofmt_xdate()

plt.xlabel('Date')
plt.ylabel('Average Price')
plt.title('Line Graph of Average Prices by Item over Time')
plt.legend()
plt.show(lj)

fig, axes = plt.subplots(1, len(database['Item'].unique()))
for item, axis in zip(master_frame.columns.to_list(), axes):
    axis.hist(master_frame[item], bins=20, alpha=0.5)
    axis.set_xlabel('Price')
    axis.set_ylabel('# Listings')
    axis.set_title(item)
plt.show()

with open(database_file, 'w', newline='') as f:
    database.to_csv(f, index=False)
    print("Data written to", database_file)
