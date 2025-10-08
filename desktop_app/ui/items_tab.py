# desktop_app/ui/items_tab.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog)
from services.api_client import APIClient
from .item_dialog import ItemDialog
from .qr_display_dialog import QRDisplayDialog

class ItemsTab(QWidget):
    def __init__(self, api_client: APIClient):
        super().__init__()
        
        self.api_client = api_client
        self.items_cache = []
        
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # --- Control Buttons ---
        control_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Item")
        self.edit_button = QPushButton("Edit Item")
        self.delete_button = QPushButton("Delete Item")
        self.qr_button = QPushButton("Generate QR Code")
        self.upload_button = QPushButton("Upload From File...")

        self.add_button.clicked.connect(self.open_add_item_dialog)
        self.edit_button.clicked.connect(self.open_edit_item_dialog)
        self.delete_button.clicked.connect(self.delete_selected_item)
        self.qr_button.clicked.connect(self.generate_item_qr)
        self.upload_button.clicked.connect(self.upload_file)
        
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.qr_button.setEnabled(False)
        
        control_layout.addWidget(self.add_button)
        control_layout.addWidget(self.edit_button)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.qr_button)
        control_layout.addWidget(self.upload_button)
        control_layout.addStretch()
        
        # --- Items Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "QR Code", "Name", "Retail Price", "Wholesale Price", "Stock", "Category"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.update_button_states)

        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.table)
        
        self.load_items()

    def load_items(self):
        """Fetch items from the API, populate the table, and cache the results."""
        self.items_cache = self.api_client.get_items(limit=2000)
        self.table.setRowCount(0)
        for row_number, item in enumerate(self.items_cache):
            self.table.insertRow(row_number)
            self.table.setItem(row_number, 0, QTableWidgetItem(str(item.get("id"))))
            self.table.setItem(row_number, 1, QTableWidgetItem(item.get("qr_code")))
            self.table.setItem(row_number, 2, QTableWidgetItem(item.get("name")))
            self.table.setItem(row_number, 3, QTableWidgetItem(str(item.get("retail_price"))))
            self.table.setItem(row_number, 4, QTableWidgetItem(str(item.get("wholesale_price"))))
            self.table.setItem(row_number, 5, QTableWidgetItem(str(item.get("stock_quantity"))))
            self.table.setItem(row_number, 6, QTableWidgetItem(item.get("category")))
        self.update_button_states()

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Item File", "", "Excel Files (*.xlsx);;CSV Files (*.csv)")
        if file_path:
            response = self.api_client.upload_items_file(file_path)
            if response and "message" in response:
                details = response.get('details', {})
                created = details.get('created', 0)
                updated = details.get('updated', 0)
                QMessageBox.information(self, "Upload Complete", f"File processed successfully.\nCreated: {created}\nUpdated: {updated}")
                self.load_items()
            else:
                error_detail = response.get("detail") if response else "An unknown error occurred."
                QMessageBox.critical(self, "Upload Failed", f"Failed to process file: {error_detail}")

    def open_add_item_dialog(self):
        dialog = ItemDialog(self.api_client, parent=self)
        if dialog.exec():
            self.load_items()

    def open_edit_item_dialog(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        item_id = int(selected_items[0].text())
        item_data = self.api_client.get_item(item_id)
        if not item_data:
            QMessageBox.critical(self, "Error", "Could not fetch item details from the server.")
            return
        dialog = ItemDialog(self.api_client, item_data=item_data, parent=self)
        if dialog.exec():
            self.load_items()
    
    def delete_selected_item(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        item_id = int(selected_items[0].text())
        item_name = selected_items[2].text()
        reply = QMessageBox.question(self, "Delete Item", 
                                     f"Are you sure you want to delete the item '{item_name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            success = self.api_client.delete_item(item_id)
            if success:
                QMessageBox.information(self, "Success", f"Item '{item_name}' was deleted.")
                self.load_items()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete the item from the server.")

    def update_button_states(self):
        is_item_selected = bool(self.table.selectedItems())
        self.edit_button.setEnabled(is_item_selected)
        self.delete_button.setEnabled(is_item_selected)
        self.qr_button.setEnabled(is_item_selected)
        
    def generate_item_qr(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        item_id = int(selected_items[0].text())
        response = self.api_client.get_item_qr(item_id)
        if response and "qr_code_image" in response:
            dialog = QRDisplayDialog(response.get("item_name"), response.get("qr_code_image"), self)
            dialog.exec()
        else:
            QMessageBox.critical(self, "Error", "Could not generate QR code from the server.")