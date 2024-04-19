from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd
import json
from json import loads

database_file = 'database.csv'

# Define the input and output CSV file names (same in this case)

try:
    # Attempt to read the existing CSV file
    database = pd.read_csv(database_file)
    print('case 1')
except ValueError:
    # If the CSV file does not exist, create an empty DataFrame
    database = pd.DataFrame(columns=['Date', 'Item', 'AveragePrice'])
    print('case 2')

items = database['Item'].unique().tolist()
print('ITEMS: ' + str(items))

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
    print(item)
    
    prices = getPricesByLink(trackedLinks[item])
    pricesWithoutOutliers = removeOutliers(prices)
    
    listings = pd.Series(pricesWithoutOutliers)
    listings.sort_values(ignore_index=True)  # Sort listings
    maximum = listings.max()
    minimum = listings.min()
    

    database[item] = listings

print(database)

with open(database_file, 'w', newline='') as f:
    database.to_csv(f, index=False)
    print("Data written to", database_file)

# Load master frame from CSV file (for testing purposes)
#try:
#    loadedMasterFrame = pd.read_csv(database_file)
#    print(loadedMasterFrame)
#except pd.errors.EmptyDataError:
#    print("No data found in ", database_file)