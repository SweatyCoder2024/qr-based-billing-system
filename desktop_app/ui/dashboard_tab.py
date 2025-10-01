# desktop_app/ui/dashboard_tab.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from services.api_client import APIClient

class DashboardTab(QWidget):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client

        main_layout = QVBoxLayout(self)

        # --- Statistics Group ---
        stats_group = QGroupBox("Today's Statistics")
        stats_layout = QVBoxLayout()
        stats_group.setLayout(stats_layout)

        self.sales_label = QLabel("Today's Sales: ₹0.00")
        self.sales_label.setFont(QFont("Arial", 14))
        self.orders_label = QLabel("Total Orders Today: 0")
        self.orders_label.setFont(QFont("Arial", 14))

        stats_layout.addWidget(self.sales_label)
        stats_layout.addWidget(self.orders_label)

        # --- Top Sellers Group ---
        top_sellers_group = QGroupBox("Top Selling Items")
        top_sellers_layout = QVBoxLayout()
        top_sellers_group.setLayout(top_sellers_layout)

        self.top_sellers_table = QTableWidget()
        self.top_sellers_table.setColumnCount(3)
        self.top_sellers_table.setHorizontalHeaderLabels(["Item Name", "Quantity Sold", "Total Revenue"])
        self.top_sellers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        top_sellers_layout.addWidget(self.top_sellers_table)

        # --- Refresh Button ---
        self.refresh_button = QPushButton("Refresh Dashboard")
        self.refresh_button.clicked.connect(self.refresh_dashboard)

        # --- Add widgets to main layout ---
        main_layout.addWidget(stats_group)
        main_layout.addWidget(top_sellers_group)
        main_layout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        self.refresh_dashboard()

    def refresh_dashboard(self):
        stats = self.api_client.get_dashboard_stats()
        if not stats:
            print("Could not fetch dashboard stats.")
            return

        self.sales_label.setText(f"Today's Sales: ₹{float(stats.get('total_revenue', 0.0)):.2f}")
        self.orders_label.setText(f"Total Orders Today: {stats.get('total_orders', 0)}")

        top_sellers = stats.get('top_sellers', [])
        self.top_sellers_table.setRowCount(0)
        for row_num, seller in enumerate(top_sellers):
            self.top_sellers_table.insertRow(row_num)
            self.top_sellers_table.setItem(row_num, 0, QTableWidgetItem(seller.get('name')))
            self.top_sellers_table.setItem(row_num, 1, QTableWidgetItem(str(seller.get('quantity_sold'))))
            self.top_sellers_table.setItem(row_num, 2, QTableWidgetItem(f"₹{float(seller.get('total_revenue')):.2f}"))