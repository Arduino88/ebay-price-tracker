import pandas as pd
import json

# program to iterate through the database and delete data for a select item

database_file = 'database.csv'

with open('tracked-links.json', 'r') as f:
    trackedLinks = json.loads(f.read())

try:
    # Attempt to read the existing CSV file
    database = pd.read_csv(database_file)
except ValueError:
    # If the CSV file does not exist, create an empty DataFrame
    database = pd.DataFrame(columns=['Date', 'Item', 'AveragePrice'])
    print('case 2')

items = database['Item'].unique().tolist()
print('DATABASE LOADED')
print('Items:', items)
print('Which item do you want to delete?')
user_input = input()
print('Are you sure? (Y/N)')
if input() == 'Y':
    if user_input in items:
        print('Deleting', user_input, 'from database.')
        database.drop(database[database['Item'] == user_input].index, inplace=True)
        database.to_csv(database_file, index=False)
        print('Database updated!')
        
    else:
        print('Item not found in database')
        
    #delete entry from tracked links
    for item in trackedLinks.keys():
        if user_input == item:
            del trackedLinks[item]
            break
else:
    print('Aborting.')

with open("tracked-links.json", "w") as f:
    json.dump(trackedLinks, f, indent=4)