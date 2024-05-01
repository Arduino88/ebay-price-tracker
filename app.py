import sys
import matplotlib
matplotlib.use('QtAgg')
import json
from PyQt6 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

import pandas as pd

database_file = 'ebay-price-tracker/database.csv'
master_frame_file ='ebay-price-tracker/master_frame.csv'

# LOAD TRACKED LINKS
with open('ebay-price-tracker/tracked-links.json', 'r') as f:
    trackedLinks = json.loads(f.read())
    
print('Tracked links loaded.')
#print(trackedLinks) #debug line

# LOAD DATABASE
try:
    # Attempt to read the existing CSV file
    database = pd.read_csv(database_file)
except ValueError:
    # If the CSV file does not exist, create an empty DataFrame
    database = pd.DataFrame(columns=['Date', 'Item', 'AveragePrice'])

print('Database loaded.')
#print(database) #debug line

# LOAD MASTER FRAME
try:
    # Attempt to read the existing CSV file
    master_frame = pd.read_csv(master_frame_file)
except ValueError:
    print('Error:', master_frame_file, 'is empty.')

print('Master frame loaded.')
#print(master_frame) #debug line

items = database['Item'].unique().tolist()


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the matplotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Create our pandas DataFrame with some simple
        # data and headers.

        # plot the pandas DataFrame, passing in the
        # matplotlib Canvas axes.
        for item in database['Item'].unique():
            item_df = database[database['Item'] == item]
            plt.plot([datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f') for date in item_df['Date']], item_df['AveragePrice'], label=item)
        
        
            item_df.plot(
                ax=sc.axes,
                kind='line',
                xlabel='Date',
                ylabel='Average Price',
                subplots=True,
                legend=False,
                title='Item Prices'
                )

        self.setCentralWidget(sc)
        self.show()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()