import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

database_file = "database.csv"
master_frame_file = (
    f"readings/master_frame_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.csv"
)
os.makedirs(master_frame_file)

try:
    # Attempt to read the existing CSV file
    database = pd.read_csv(database_file)
except FileNotFoundError:
    # If the CSV file does not exist, create an empty DataFrame
    database = pd.DataFrame(columns=["Date", "Item", "AveragePrice"])
    print(database_file, "is empty; setting default columns.")

print("Database loaded.")

items = database["Item"].unique().tolist()


# initialize master_frame
master_frame = pd.DataFrame(columns=items)

with open("tracked-links.json", "r") as f:
    trackedLinks = json.loads(f.read())


def getPricesByLink(
    link: str,
) -> list:  # Returns list of prices scraped from a given ebay link
    if "mercari" in link:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        r = requests.get(link, headers=headers)
    else:
        r = requests.get(link)

    print(r.text)

    html_content = BeautifulSoup(r.text, "html.parser")
    itemPrices = []

    if "ebay" in link:
        searchResults = html_content.find("ul", {"class": "srp-results"}).find_all(
            "li", {"class": "s-item"}
        )

        for result in searchResults:
            priceAsText = result.find("span", {"class": "s-item__price"}).text
            if "to" in priceAsText:
                continue
            price = float(
                priceAsText[3:].replace(",", "")
            )  # Remove commas and convert to float
            itemPrices.append(price)
        return itemPrices

    if "mercari" in link:
        test = html_content.select('div[data-testid="SearchResults"]')
        print(test)
        searchResults = html_content.find(
            "div", {"data-testid": "SearchResults"}
        ).find_all("div", {"data-testid": "ProductThumbWrapper"})

        for result in searchResults:
            priceAsText = result.find(
                "p", {"data-testid": "ProductThumbItemPrice"}
            ).text
            price = float(
                priceAsText.strip().replace(",", "").replace("$", "")
            )  # Remove commas and convert to float
            itemPrices.append(price)
        return itemPrices


def removeOutliers(prices: list, m=2) -> list:
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def getAverage(prices: list) -> float:
    return np.mean(prices)


for item in trackedLinks.keys():
    print("Scraping prices for", item + "...")
    prices = getPricesByLink(trackedLinks[item])
    listings = pd.Series(removeOutliers(prices))
    maximum = listings.max()
    minimum = listings.min()
    averagePrice = getAverage(listings)
    new_row_df = pd.DataFrame(
        [{"Date": datetime.now(), "Item": item, "AveragePrice": averagePrice}]
    )
    database = pd.concat([database, new_row_df], ignore_index=True)

    master_frame[item] = listings

with open(database_file, "w", newline="") as f:
    database.to_csv(f, index=False)
    print("Average price data written to", database_file + ".")

with open(master_frame_file, "w", newline="") as f:
    master_frame.to_csv(f, index=False)
    print("Masterframe written to", master_frame_file + ".")

# print(master_frame)

# Load master frame from CSV file (for testing purposes)
# try:
#    loadedMasterFrame = pd.read_csv(master_frame_file)
#    print(loadedMasterFrame)
# except pd.errors.EmptyDataError:
#    print("No data found in ", master_frame_file)
