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
print('DATABASE LOADED: ' + str(database))


#initialize master_frame
master_frame = pd.DataFrame(columns=items)
print(master_frame)

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
    listings = pd.Series(removeOutliers(prices))
    listings.sort_values(kind='mergesort', ignore_index=True)   # Sort listings
    maximum = listings.max()
    minimum = listings.min()
    averagePrice = getAverage(listings)
    new_row_df = pd.DataFrame([{'Date': datetime.now(), 'Item': item, 'AveragePrice': averagePrice}])
    database = pd.concat([database, new_row_df], ignore_index=True)
    
    master_frame[item] = listings
    print(master_frame)

print(database)



# Assuming 'database' is your DataFrame and 'Date' and 'AveragePrice' are the columns you want to plot

plt.figure(figsize=(10, 6))  # Set the figure size

for item in database['Item'].unique():
    item_df = database[database['Item'] == item]

    plt.plot([datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f') for date in item_df['Date']], item_df['AveragePrice'], label=item)

# Format the x-axis with dates
date_formatter = mdates.DateFormatter('%Y-%m-%d')
plt.gca().xaxis.set_major_formatter(date_formatter)
plt.gcf().autofmt_xdate()

plt.xlabel('Date')  # Set the x-axis label
plt.ylabel('Average Price')  # Set the y-axis label
plt.title('Line Graph of Average Prices by Item over Time')  # Set the title
plt.legend()  # Add a legend
plt.show()  # Show the plot




# Assuming 'master_frame' is your DataFrame
for item in master_frame.columns.to_list():
    # Create a new figure for each histogram
    fig, ax = plt.subplots()
    
    # Plot the histogram
    ax.hist(master_frame[item], bins=30, alpha=0.5)
    plt.title(item +' Market Overview')
    plt.xlabel('Price')
    plt.ylabel('# Listings')
    # Show the histogram
    plt.show()



with open(database_file, 'w', newline='') as f:
    database.to_csv(f, index=False)
    print("Data written to", database_file)

