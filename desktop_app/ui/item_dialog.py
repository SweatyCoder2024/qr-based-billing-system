# desktop_app/ui/item_dialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QDialogButtonBox, QSpinBox, QDoubleSpinBox, QMessageBox)
from services.api_client import APIClient
from typing import Optional, Dict

class ItemDialog(QDialog):
    def __init__(self, api_client: APIClient, item_data: Optional[Dict] = None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.item_data = item_data # Will be None for "Add", populated for "Edit"

        # Set title based on whether we are adding or editing
        self.setWindowTitle("Edit Item" if self.item_data else "Add New Item")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.qr_code_input = QLineEdit()
        self.retail_price_input = QDoubleSpinBox()
        self.retail_price_input.setMaximum(999999.99)
        self.wholesale_price_input = QDoubleSpinBox()
        self.wholesale_price_input.setMaximum(999999.99)
        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(999999)
        self.category_input = QLineEdit()

        form_layout.addRow("Name*:", self.name_input)
        form_layout.addRow("Barcode (QR Code):", self.qr_code_input)
        form_layout.addRow("Retail Price*:", self.retail_price_input)
        form_layout.addRow("Wholesale Price:", self.wholesale_price_input)
        form_layout.addRow("Stock Quantity:", self.stock_input)
        form_layout.addRow("Category:", self.category_input)

        # If we are editing, populate the fields with existing data
        if self.item_data:
            self.populate_form()
            # Barcode should not be editable for an existing item
            self.qr_code_input.setReadOnly(True)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)

    def populate_form(self):
        """Fills the form fields with data from an existing item."""
        self.name_input.setText(self.item_data.get("name", ""))
        self.qr_code_input.setText(self.item_data.get("qr_code", ""))
        self.retail_price_input.setValue(float(self.item_data.get("retail_price", 0.0)))
        self.wholesale_price_input.setValue(float(self.item_data.get("wholesale_price", 0.0)))
        self.stock_input.setValue(self.item_data.get("stock_quantity", 0))
        self.category_input.setText(self.item_data.get("category", ""))

    def get_item_data_from_form(self):
        data = {
            "name": self.name_input.text(),
            "retail_price": str(self.retail_price_input.value()),
            "wholesale_price": str(self.wholesale_price_input.value()),
            "stock_quantity": self.stock_input.value(),
            "category": self.category_input.text() or None
        }
        # Only include qr_code if we are in "Add" mode
        if not self.item_data:
            data["qr_code"] = self.qr_code_input.text() or None
        return data

    def accept(self):
        """Handles both creating and updating an item."""
        item_data = self.get_item_data_from_form()
        if not item_data["name"]:
            QMessageBox.warning(self, "Input Error", "Name is a required field.")
            return

        if self.item_data: # If we are in "Edit" mode
            item_id = self.item_data.get("id")
            response = self.api_client.update_item(item_id, item_data)
            action = "updated"
        else: # If we are in "Add" mode
            response = self.api_client.create_item(item_data)
            action = "created"

        if response and "id" in response:
            QMessageBox.information(self, "Success", f"Item '{response['name']}' was {action} successfully.")
            super().accept()
        else:
            error_detail = response.get("detail") if response else "An unknown error occurred."
            QMessageBox.critical(self, "Error", f"Failed to {action} item: {error_detail}")