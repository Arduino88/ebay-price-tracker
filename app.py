## UNFINISHED ##


import sys

import matplotlib

matplotlib.use("QtAgg")
import json

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6 import QtWidgets

database_file = "database.csv"
master_frame_file = "master_frame.csv"

# LOAD TRACKED LINKS
with open("tracked-links.json", "r") as f:
    trackedLinks = json.loads(f.read())

print("Tracked links loaded.")
# print(trackedLinks) #debug line

# LOAD DATABASE
try:
    # Attempt to read the existing CSV file
    database = pd.read_csv(database_file)
except ValueError:
    # If the CSV file does not exist, create an empty DataFrame
    database = pd.DataFrame(columns=["Date", "Item", "AveragePrice"], dtype=str)

print("Database loaded.")
# print(database) #debug line

# LOAD MASTER FRAME
try:
    # Attempt to read the existing CSV file
    master_frame = pd.read_csv(master_frame_file)
except ValueError:
    print("Error:", master_frame_file, "is empty.")

print("Master frame loaded.")
# print(master_frame) #debug line

items = database["Item"].unique().tolist()


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        colors = ("red", "orange", "green", "blue", "purple", "black")

        for i, item in enumerate(database["Item"].unique()):
            i %= len(colors)
            item_df = database[database["Item"] == item]
            item_df["Date"] = (pd.to_datetime(item_df["Date"]),)
            plt.plot(
                item_df["AveragePrice"],
                label=item,
            )

            if isinstance(item_df, pd.DataFrame):
                item_df = item_df.rename(columns={"AveragePrice": item})
                item_df = item_df.drop("Item", axis=1)
            else:
                print(
                    f"ERROR: item_df is not a Pandas DataFrame, item_df type: {type(item_df)}"
                )

            print(item_df)

            item_df.plot(
                ax=sc.axes,
                kind="line",
                color=colors[i],
                xlabel="Date",
                ylabel="Average Price",
                subplots=True,
                legend=True,
                title="Item Prices",
            )

        plt.legend(database["Item"].unique())
        self.setCentralWidget(sc)
        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
