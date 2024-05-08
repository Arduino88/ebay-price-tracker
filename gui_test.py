from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt6.QtCore import QSize, Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Ebay Price Tracker")
        button = QPushButton("Click Me!")
        
        self.setFixedSize(QSize(400, 300))
        
        self.setCentralWidget(button)







app = QApplication()


window = MainWindow()
window.show()

# Start the event loop.
app.exec()

