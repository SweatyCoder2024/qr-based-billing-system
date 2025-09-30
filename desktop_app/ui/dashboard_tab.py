# desktop_app/ui/dashboard_tab.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        label = QLabel("This is the Dashboard Tab")
        label.setFont(QFont("Arial", 16))
        layout.addWidget(label)
        self.setLayout(layout)