# desktop_app/ui/items_tab.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from services.api_client import APIClient
from .item_dialog import ItemDialog

class ItemsTab(QWidget):
    def __init__(self, api_client: APIClient):
        super().__init__()

        self.api_client = api_client

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Control Buttons ---
        control_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.open_add_item_dialog)

        self.edit_button = QPushButton("Edit Item")
        self.edit_button.clicked.connect(self.open_edit_item_dialog)
        self.edit_button.setEnabled(False)

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.clicked.connect(self.delete_selected_item) # <-- CONNECT THE BUTTON
        self.delete_button.setEnabled(False)

        self.qr_button = QPushButton("Generate QR Code")

        control_layout.addWidget(self.add_button)
        control_layout.addWidget(self.edit_button)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.qr_button)
        control_layout.addStretch()

        # --- Items Table ---
        self.table = QTableWidget()
        # ... (table setup is unchanged)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "QR Code", "Name", "Retail Price", 
            "Wholesale Price", "Stock", "Category"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.update_button_states)

        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.table)

        self.load_items()

    def load_items(self):
        # ... (this function is unchanged)
        items = self.api_client.get_items(limit=1000)
        self.table.setRowCount(0)
        for row_number, item in enumerate(items):
            self.table.insertRow(row_number)
            self.table.setItem(row_number, 0, QTableWidgetItem(str(item.get("id"))))
            self.table.setItem(row_number, 1, QTableWidgetItem(item.get("qr_code")))
            self.table.setItem(row_number, 2, QTableWidgetItem(item.get("name")))
            self.table.setItem(row_number, 3, QTableWidgetItem(str(item.get("retail_price"))))
            self.table.setItem(row_number, 4, QTableWidgetItem(str(item.get("wholesale_price"))))
            self.table.setItem(row_number, 5, QTableWidgetItem(str(item.get("stock_quantity"))))
            self.table.setItem(row_number, 6, QTableWidgetItem(item.get("category")))
        self.update_button_states()

    def open_add_item_dialog(self):
        # ... (this function is unchanged)
        dialog = ItemDialog(self.api_client, parent=self)
        if dialog.exec():
            self.load_items()

    def open_edit_item_dialog(self):
        # ... (this function is unchanged)
        selected_items = self.table.selectedItems()
        if not selected_items: return
        item_id = int(selected_items[0].text())
        item_data = self.api_client.get_item(item_id)
        if not item_data:
            QMessageBox.critical(self, "Error", "Could not fetch item details from the server.")
            return
        dialog = ItemDialog(self.api_client, item_data=item_data, parent=self)
        if dialog.exec():
            self.load_items()

    # --- NEW FUNCTION TO DELETE AN ITEM ---
    def delete_selected_item(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        item_id = int(selected_items[0].text())
        item_name = selected_items[2].text() # Get name for confirmation message

        # Show a confirmation dialog
        reply = QMessageBox.question(self, "Delete Item", 
                                     f"Are you sure you want to delete the item '{item_name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            success = self.api_client.delete_item(item_id)
            if success:
                QMessageBox.information(self, "Success", f"Item '{item_name}' was deleted.")
                self.load_items() # Refresh the list
            else:
                QMessageBox.critical(self, "Error", "Failed to delete the item from the server.")

    def update_button_states(self):
        # ... (this function is unchanged)
        is_item_selected = bool(self.table.selectedItems())
        self.edit_button.setEnabled(is_item_selected)
        self.delete_button.setEnabled(is_item_selected)