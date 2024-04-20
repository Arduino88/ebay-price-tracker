from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import pandas as pd
import json
import sys
import pandas as pd
import json
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QWidget,
)

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

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QHBoxLayout Example")

        # Create a QHBoxLayout instance
        layout = QHBoxLayout()

        # Add widgets to the layout
        layout.addWidget(QPushButton("Left-Most"), 1)
        layout.addWidget(QPushButton("Center"), 1)
        self.item_combo_box = QComboBox()
        
        #add all items from tracked-links to combo box
        for item in items:
            self.item_combo_box.addItem(item)
        layout.addWidget(self.item_combo_box, 1)

        # Set the layout on the application's window
        self.setLayout(layout)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()

    window.show()


app.exec()

with open("tracked-links.json", "w") as f:
    json.dump(trackedLinks, f, indent=4)