# desktop_app/ui/billing_tab.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QListWidget, QListWidgetItem)
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from services.api_client import APIClient
import base64
from typing import Optional # <-- This import was likely missing or incomplete

class BillingTab(QWidget):
    session_created = pyqtSignal(str)

    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.active_sessions_cache = {}

        main_layout = QHBoxLayout(self)
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)

        # --- Left Panel (Bill/Session List) ---
        left_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        sessions_label = QLabel("Active Bills")
        sessions_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        self.sessions_list = QListWidget()
        self.sessions_list.currentItemChanged.connect(self.on_session_selected)

        new_bill_button = QPushButton("Create New Bill")
        new_bill_button.clicked.connect(self.create_new_bill_session)

        self.qr_image_label = QLabel("Select a bill to see its QR code")
        self.qr_image_label.setFixedSize(250, 250)
        self.qr_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_panel.addWidget(sessions_label)
        left_panel.addWidget(self.sessions_list)
        left_panel.addWidget(new_bill_button)
        left_panel.addWidget(self.qr_image_label)

        # --- Right Panel (Order Display) ---
        order_title_label = QLabel("Selected Bill Details")
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

        self.load_active_sessions()

    def load_active_sessions(self):
        """Fetches all active sessions and populates the list."""
        self.sessions_list.clear()
        self.active_sessions_cache.clear()
        sessions = self.api_client.get_active_sessions()
        for session in sessions:
            session_id = session.get("session_id")
            self.active_sessions_cache[session_id] = session
            item = QListWidgetItem(f"Bill #{session.get('id')}")
            item.setData(Qt.ItemDataRole.UserRole, session_id)
            self.sessions_list.addItem(item)

    def create_new_bill_session(self):
        """Creates a new bill/session and refreshes the list."""
        new_session = self.api_client.create_session()
        if new_session:
            self.load_active_sessions()
            for i in range(self.sessions_list.count()):
                item = self.sessions_list.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == new_session.get("session_id"):
                    self.sessions_list.setCurrentItem(item)
                    break

    def on_session_selected(self, current_item: QListWidgetItem, previous_item: QListWidgetItem):
        """Called when the user clicks on a bill in the list."""
        if not current_item:
            self.qr_image_label.setText("Select or create a bill.")
            self.update_order_display(None)
            return

        session_id = current_item.data(Qt.ItemDataRole.UserRole)
        session_data = self.active_sessions_cache.get(session_id)

        if session_data:
            qr_base64 = session_data.get("qr_code")
            # This logic seems flawed, let's simplify and always fetch for now
            fetched_session = self.api_client.get_session_qr(session_id)
            if fetched_session:
                qr_base64 = fetched_session.get("qr_code")
                image_data = base64.b64decode(qr_base64)
                pixmap = QPixmap.fromImage(QImage.fromData(image_data, "PNG"))
                self.qr_image_label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

            self.session_created.emit(session_id)

            order_data = self.api_client.get_order_for_session(session_id)
            self.update_order_display(order_data)

    @pyqtSlot(dict)
    def handle_websocket_message(self, message: dict):
        if message.get("type") == "order_update" or message.get("type") == "new_order_created":
            order_data = message.get("data")
            if order_data:
                current_item = self.sessions_list.currentItem()
                if current_item and current_item.data(Qt.ItemDataRole.UserRole) == order_data.get("session_id"):
                    self.update_order_display(order_data)
                # If a new order was created, we should refresh the whole list
                if message.get("type") == "new_order_created":
                    self.load_active_sessions()


    def update_order_display(self, order_data: Optional[dict]):
        self.order_table.setRowCount(0)
        if not order_data:
            self.total_label.setText("Total: ₹0.00")
            return

        items = order_data.get("items", [])
        for row_num, item in enumerate(items):
            self.order_table.insertRow(row_num)
            self.order_table.setItem(row_num, 0, QTableWidgetItem(item.get("item", {}).get("name")))
            self.order_table.setItem(row_num, 1, QTableWidgetItem(str(item.get("quantity"))))
            self.order_table.setItem(row_num, 2, QTableWidgetItem(f"₹{float(item.get('unit_price', 0)):.2f}"))
            total_item_price = float(item.get('unit_price', 0)) * item.get('quantity', 0)
            self.order_table.setItem(row_num, 3, QTableWidgetItem(f"₹{total_item_price:.2f}"))
        self.total_label.setText(f"Total: ₹{float(order_data.get('total_amount', 0.0)):.2f}")