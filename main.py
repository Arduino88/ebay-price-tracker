from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime
import pandas as pd
import json

f = open('database.json', 'r')
jsonString = f.read()
parsedDict = json.loads(jsonString)
f.close()
    
trackedLinks = { #format: file as key, link as value
    '1996retroNuptseBlack': 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw=north+face+1996+retro+neptuse+black&_sacat=57988&LH_BIN=1&rt=nc&LH_ItemCondition=1000&_ipg=120',
    '3090': 'https://www.ebay.ca/sch/i.html?_nkw=rtx+3090&Brand=&_dcat=27386&LH_BIN=1&rt=nc&LH_ItemCondition=1500%7C2010%7C2020%7C1000&_ipg=120',
    '3080': 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw=rtx+3080&_sacat=0&LH_BIN=1&rt=nc&LH_ItemCondition=1000%7C1500%7C2010&_ipg=120',
    #'fenderStratocaster': 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw=fender+stratocaster&_sacat=0&LH_BIN=1&rt=nc&LH_PrefLoc=1',
    'yeezy350': 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw=yeezy+boost+350+zebra&_sacat=15709&US%2520Shoe%2520Size=9&_dcat=15709&_ipg=120',
    'air max 270': 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw=nike+air+max+270&_sacat=15709&LH_ItemCondition=1000&rt=nc&LH_BIN=1&US%2520Shoe%2520Size=9&_dcat=15709',
}

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