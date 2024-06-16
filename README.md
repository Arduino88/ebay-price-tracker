### Ebay-Price-Tracker
---
A simple webscraping application used to log prices of Ebay listings.
This is currently unfinished, but has working price logging and graphing functionality, as well as persistence.
Webscraping is done with the BeautifulSoup library.
Data analysis and manipulation is done with Pandas, NumPy and Matplotlib.

## Instructions
1. Create a .json file with the name `tracked-links.json` in the main directory.
   - The contents of this file should be in the following format:
```json
    {
    "item1_name": "item1_link",
    "item2_name": "item2_link",
    "item3_name": "item3_link"
    }
```

2. Create a folder called `readings` in the main directory - this will be filled with the scraped data in the form of .csv files.

3. Run either `tempMain.py` (for scraping and visual graphing) or `updateData.py` (for background operation and logging).

 
---

I am investigating the possibility of creating a script to run updateData.py automatically in the background but have not gotten around to it.

I hope you like my project, PRs are welcome, I just might take a bit to review them as I am a student :)
