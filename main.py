from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd
import json #does this need to be stated twice?
from json import loads, dumps
import os.path

d = { #starter dictionary for database.json, this needs to be tested
    "1996retroNuptseBlack": {}, 
     "3090": {}, 
     "3080": {}, 
     "fenderStratocaster": {}, 
     "yeezy350": {}, 
     "air max 270": {}
}

#tempData = pd.read_csv('database.csv', parse_dates=['Date'])
#tempData.set_index('Date')
#print(tempData)

if os.path.isfile('database.json'):
    with open('database.json', 'r') as f:
        parsedDict = json.loads(f.read())
  
    dictKey = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

else:
    raise Exception('database.json not found')

#parsedDict = d

if os.path.isfile('tracked-links.json'):
    with open('tracked-links.json', 'r') as f:
        trackedLinks = json.loads(f.read())

else:
    raise Exception('tracked-links.json not found')


masterFrame = pd.DataFrame()

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

def writeToDict(product, meanPrice):
    parsedDict[product][dictKey] = round(meanPrice, 2)

for product in parsedDict.keys():
    
    print(product)
    
    prices = getPricesByLink(trackedLinks[product])
    pricesWithoutOutliers = removeOutliers(prices)
    
    listings = pd.Series(pricesWithoutOutliers)
    listings = listings.sort_values(kind='mergesort', ignore_index=True)
    
    maximum = listings.max()
    minimum = listings.min()
    
    writeToDict(product, listings.mean())
    masterFrame[product] = listings
    
print(masterFrame)
masterFrame.plot.hist(bins=30, alpha=0.5)
plt.show()

masterFrame.plot(kind='box')

#tempData=pd.DataFrame(data=pd.to_datetime(parsedDict)) # double temporary lmfao



saveData = pd.DataFrame(data=parsedDict) #temporary

#saveData.index.rename('Date')

print(saveData)

saveData.plot(subplots=True)
plt.show()

s = open('database.json', 'w')
result = saveData.to_json()
parsed = loads(result)
s.write(dumps(parsed, indent=4))
s.close()

s = open('tracked-links.json', 'w')
linkJson = json.dumps(trackedLinks)
s.write(linkJson)
s.close()


saveData.to_csv('database.csv', mode='w', date_format='%s')