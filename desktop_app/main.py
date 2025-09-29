# desktop_app/main.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Billing System")
        self.setGeometry(100, 100, 1200, 800) # x, y, width, height

        # Add a simple label
        self.label = QLabel("Welcome to the QR Billing System!", self)
        self.label.setFont(QFont("Arial", 18))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the label to be the main widget of the window
        self.setCentralWidget(self.label)


if __name__ == "__main__":
    # This is the entry point of our application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())