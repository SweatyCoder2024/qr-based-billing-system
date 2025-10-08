# desktop_app/ui/billing_tab.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from services.api_client import APIClient
import base64

class BillingTab(QWidget):
    session_created = pyqtSignal(str)

    def __init__(self, api_client: APIClient):
        super().__init__()

        self.api_client = api_client
        self.session_id = None

        main_layout = QHBoxLayout(self)
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)

        left_panel.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        title_label = QLabel("Scan to Connect Mobile")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.qr_image_label = QLabel("Generating QR Code...")
        self.qr_image_label.setFixedSize(250, 250)
        self.qr_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.refresh_button = QPushButton("Refresh QR")

        left_panel.addWidget(title_label)
        left_panel.addWidget(self.qr_image_label)
        left_panel.addWidget(self.refresh_button)

        order_title_label = QLabel("Current Order")
        order_title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Unit Price", "Total Price"])
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.total_label = QLabel("Total: ₹0.00")
        self.total_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        right_panel.addWidget(order_title_label)
        right_panel.addWidget(self.order_table)
        right_panel.addWidget(self.total_label)

        self.refresh_button.clicked.connect(self.generate_session_qr)
        self.generate_session_qr()

    def generate_session_qr(self):
        session_data = self.api_client.create_session()
        if not session_data:
            QMessageBox.critical(self, "Error", "Could not create a session.")
            return
        self.session_id = session_data.get("session_id")
        qr_base64 = session_data.get("qr_code")
        image_data = base64.b64decode(qr_base64)
        pixmap = QPixmap.fromImage(QImage.fromData(image_data, "PNG"))
        self.qr_image_label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        self.session_created.emit(self.session_id)

    @pyqtSlot(dict)
    def handle_websocket_message(self, message: dict):
        if message.get("type") == "order_update":
            order_data = message.get("data")
            if order_data:
                self.update_order_display(order_data)

    def update_order_display(self, order_data: dict):
        self.order_table.setRowCount(0)
        items = order_data.get("items", [])
        for row_num, item in enumerate(items):
            self.order_table.insertRow(row_num)
            self.order_table.setItem(row_num, 0, QTableWidgetItem(item.get("item", {}).get("name")))
            self.order_table.setItem(row_num, 1, QTableWidgetItem(str(item.get("quantity"))))
            self.order_table.setItem(row_num, 2, QTableWidgetItem(f"₹{float(item.get('unit_price', 0)):.2f}"))
            total_item_price = float(item.get('unit_price', 0)) * item.get('quantity', 0)
            self.order_table.setItem(row_num, 3, QTableWidgetItem(f"₹{total_item_price:.2f}"))
        self.total_label.setText(f"Total: ₹{float(order_data.get('total_amount', 0.0)):.2f}")