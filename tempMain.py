from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd
import json #does this need to be stated twice?
from json import loads, dumps

#import data from database.csv as dataframe
database = pd.read_csv('database.csv')
database.set_index('date')

# Initialize master frame
masterFrame = pd.DataFrame(columns=['date', 'averagePrice', 'item'])
items = masterFrame['item'].unique().tolist()

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

def writeToDataFrame(product, meanPrice):
    masterFrame.loc[product] = [meanPrice]

for item in items:
    print(item)
    
    prices = getPricesByLink(trackedLinks[item])
    pricesWithoutOutliers = removeOutliers(prices)
    
    listings = pd.Series(pricesWithoutOutliers)
    listings.sort_values(kind='mergesort', ignore_index=True)  # Sort listings
    maximum = listings.max()
    minimum = listings.min()
    
    writeToDataFrame(item, getAverage(listings))
    masterFrame[item] = listings

print(masterFrame)

# Save master frame to CSV file
masterFrame.to_csv('database.csv', mode='w')

# Load master frame from CSV file (for testing purposes)
loadedMasterFrame = pd.read_csv('database.csv')
print(loadedMasterFrame)