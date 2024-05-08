import sys
import matplotlib
matplotlib.use('QtAgg')
import json
from PyQt6 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import pandas as pd

database_file = 'database.csv'
master_frame_file ='master_frame.csv'

with open('tracked-links.json', 'r') as f:
    trackedLinks = json.loads(f.read())
    
print('Tracked links loaded.')
#print(trackedLinks) #debug line

try:
    # Attempt to read the existing CSV file
    database = pd.read_csv(database_file)
except ValueError:
    # If the CSV file does not exist, create an empty DataFrame
    database = pd.DataFrame(columns=['Date', 'Item', 'AveragePrice'])

print('Database loaded.')
#print(database) #debug line

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

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Create our pandas DataFrame with some simple
        # data and headers.

        # plot the pandas DataFrame, passing in the
        # matplotlib Canvas axes.
        master_frame.plot(ax=sc.axes, kind='hist')

        self.setCentralWidget(sc)
        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()