from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import pandas as pd
import json
from json import loads

database_file = 'database.csv'
master_frame_file ='master_frame.csv'

try:
    # Attempt to read the existing CSV file
    database = pd.read_csv(database_file)
except ValueError:
    # If the CSV file does not exist, create an empty DataFrame
    database = pd.DataFrame(columns=['Date', 'Item', 'AveragePrice'])
    print(database_file, 'is empty; setting default columns.')

print('Database loaded.')

items = database['Item'].unique().tolist()


#initialize master_frame
master_frame = pd.DataFrame(columns=items)

with open('tracked-links.json', 'r') as f:
    trackedLinks = json.loads(f.read())

def getPricesByLink(link: str) -> list: # Returns list of prices scraped from a given ebay link
    r = requests.get(link)
    # Parse HTML
    pageParse = BeautifulSoup(r.text, "html.parser")
    # Narrow list items
    searchResults = pageParse.find('ul', {'class': 'srp-results'}).find_all("li", {'class': 's-item'})
    
    itemPrices = []
    
    for result in searchResults:
        priceAsText = result.find('span', {'class': 's-item__price'}).text
        if 'to' in priceAsText:
            continue
        price = float(priceAsText[3:].replace(',', ''))  # Remove commas and convert to float
        itemPrices.append(price)
    return itemPrices

def removeOutliers(prices: list, m=2) -> list:
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def getAverage(prices: list) -> float:
    return np.mean(prices)



for item in trackedLinks.keys():
    print('Scraping prices for', item + '...')
    prices = getPricesByLink(trackedLinks[item])
    listings = pd.Series(removeOutliers(prices))
    maximum = listings.max()
    minimum = listings.min()
    averagePrice = getAverage(listings)
    new_row_df = pd.DataFrame([{'Date': datetime.now(), 'Item': item, 'AveragePrice': averagePrice}])
    database = pd.concat([database, new_row_df], ignore_index=True)
    
    master_frame[item] = listings

with open(database_file, 'w', newline='') as f:
    database.to_csv(f, index=False)
    print("Average price data written to", database_file + '.')
    
with open(master_frame_file, 'w', newline='') as f:
    master_frame.to_csv(f, index=False)
    print("Masterframe written to", master_frame_file + '.')

print(master_frame)

# Load master frame from CSV file (for testing purposes)
try:
    loadedMasterFrame = pd.read_csv(master_frame_file)
    print(loadedMasterFrame)
except pd.errors.EmptyDataError:
    print("No data found in ", master_frame_file)