from bs4 import BeautifulSoup
import requests
import numpy as np
import csv
from datetime import datetime

LINK = "https://www.ebay.ca/sch/i.html?_nkw=rtx+3090&Brand=&_dcat=27386&LH_BIN=1&rt=nc&LH_ItemCondition=1500%7C2010%7C2020%7C1000"

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

def saveToFile(prices):
    fields = [datetime.today().strftime('%B-%D-%Y'), np.around(getAverage(prices), 2)]
    with open('prices.csv', 'a', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == '__main__':
    prices = getPricesByLink(LINK)
    pricesWithoutOutliers = removeOutliers(prices)
    print(getAverage(pricesWithoutOutliers))
    saveToFile(prices)