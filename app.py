import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.state=True
        
        self.button = QPushButton('Click Me!')
        self.button.setCheckable(True)
        self.button.released.connect(self.on_release)
        self.button.setChecked(self.state)
        
        # set the central widget
        self.setCentralWidget(self.button)
        
    def on_release(self):
        self.state = self.button.isChecked()    
        print(self.state)
    
    def on_click(self):
        print('clicked')
        
    def toggled(self, state):
        print('checked?', state)
        self.state = state
        
        print(self.state)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()