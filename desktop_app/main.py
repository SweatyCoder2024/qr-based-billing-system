# desktop_app/main.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget

from ui.billing_tab import BillingTab
from ui.items_tab import ItemsTab
from ui.dashboard_tab import DashboardTab
from services.api_client import APIClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Billing System")
        self.setGeometry(100, 100, 1200, 800)

        self.api_client = APIClient(base_url="http://localhost:8000")

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Pass the api_client instance to BOTH the Billing and Items tabs
        self.billing_tab = BillingTab(self.api_client) # <-- PASS THE CLIENT HERE
        self.items_tab = ItemsTab(self.api_client)
        self.dashboard_tab = DashboardTab()

        self.tabs.addTab(self.billing_tab, "Billing")
        self.tabs.addTab(self.items_tab, "Item Management")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        self.setCentralWidget(self.tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())