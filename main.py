from bs4 import BeautifulSoup
import requests
import numpy as np
import csv
from datetime import datetime

trackedLinks = { #format: file as key, link as value
    '3090.csv': 'https://www.ebay.ca/sch/i.html?_nkw=rtx+3090&Brand=&_dcat=27386&LH_BIN=1&rt=nc&LH_ItemCondition=1500%7C2010%7C2020%7C1000',
    '3080.csv': 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw=rtx+3080&_sacat=0&LH_BIN=1&rt=nc&LH_ItemCondition=1000%7C1500%7C2010',
    'fenderStratocaster.csv': 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw=fender+stratocaster&_sacat=0',
    'yeezy350.csv': 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw=yeezy+boost+350+zebra&_sacat=15709&US%2520Shoe%2520Size=9&_dcat=15709',
    'air max 270.csv': 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw=nike+air+max+270&_sacat=15709&LH_ItemCondition=1000&rt=nc&LH_BIN=1&US%2520Shoe%2520Size=9&_dcat=15709'
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
    fields = [datetime.today().strftime('%B-%D-%Y'), datetime.now().strftime('%H:%M:%S'), np.around(getAverage(prices), 2)]
    print('Average Price: ' + str(np.around(getAverage(prices))) + '\n')
    with open(file, 'a', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def recordPrice(link: str, file: str):
    prices = getPricesByLink(link)
    pricesWithoutOutliers = removeOutliers(prices)
    saveToFile(pricesWithoutOutliers, file)
    
for item in trackedLinks.keys():
    print(item)
    recordPrice(trackedLinks[item], str(item))