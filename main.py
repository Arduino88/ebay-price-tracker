from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime
import pandas as pd
import json

f = open('database.json', 'r')
parsedDict = json.loads(f.read())
f.close()
    
f = open('tracked-links.json', 'r')
trackedLinks = json.loads(f.read())
f.close()

print(parsedDict.keys())

def getPricesByLink(link):
    r = requests.get(link)
    #parse
    pageParse = BeautifulSoup(r.text, "html.parser")
    #narrow list items
    searchResults = pageParse.find('ul', {'class':'srp-results'}).find_all("li",{'class':'s-item'})
    
    itemPrices = []
    
    for result in searchResults:
        priceAsText = result.find('span', {'class':'s-item__price'}).text
        if 'to' in priceAsText:
            continue
        price = float(priceAsText[3:].replace(',',''))
        itemPrices.append(price)
    return itemPrices

def removeOutliers(prices, m=2):
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def getAverage(prices):
    return np.mean(prices)

def saveToFile(prices, file: str):
    fields = [datetime.today().strftime(), datetime.now().strftime('%H:%M:%S'), np.around(getAverage(prices), 2)]
    print('Average Price: ' + str(np.around(getAverage(prices))) + '\n')
    with open(file + '.csv', 'a', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


    

masterFrame = pd.DataFrame()

for product in trackedLinks.keys():
    
    #dfHistory = pd.read_csv(product + '.csv', index_col='date', parse_dates=['date'])
    
    
    #print(product)
    
    prices = getPricesByLink(trackedLinks[product])
    pricesWithoutOutliers = removeOutliers(prices)
    
    listings = pd.Series(pricesWithoutOutliers)
    listings = listings.sort_values(kind='mergesort', ignore_index=True)
    
    #saveToFile(pricesWithoutOutliers, product)
    maximum = listings.max()
    minimum = listings.min()
    #print(listings)
    #print('max: ' + '%.2f' % maximum + ', min: ' + '%.2f' % minimum + ', mean: ' + '%.2f' % listings.mean())
    #histogram(listings, product)
    masterFrame.insert(0, product, listings)
    
    
       
print(masterFrame)
masterFrame.plot.hist(bins=30, alpha=0.5)
plt.show()


s = open('tracked-links.json', 'w')
linkJson = json.dumps(trackedLinks)
s.write(linkJson)
s.close()