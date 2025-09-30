# desktop_app/ui/billing_tab.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtCore import Qt
from services.api_client import APIClient
import base64

class BillingTab(QWidget):
    def __init__(self, api_client: APIClient):
        super().__init__()

        self.api_client = api_client
        self.session_id = None

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(main_layout)

        # --- QR Code Display ---
        title_label = QLabel("Scan to Connect Mobile")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        self.qr_image_label = QLabel("Generating QR Code...")
        self.qr_image_label.setFixedSize(250, 250) # Make the QR code a nice size
        self.qr_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.refresh_button = QPushButton("Refresh QR")
        self.refresh_button.clicked.connect(self.generate_session_qr)

        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(self.qr_image_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # --- Generate the first QR code ---
        self.generate_session_qr()

    def generate_session_qr(self):
        """Fetch a new session and display the QR code."""
        self.qr_image_label.setText("Generating QR Code...")
        session_data = self.api_client.create_session()

        if not session_data:
            QMessageBox.critical(self, "Error", "Could not connect to the backend to create a session.")
            self.qr_image_label.setText("Connection Failed")
            return

        self.session_id = session_data.get("session_id")
        qr_base64 = session_data.get("qr_code")

        # Decode the base64 string into an image
        image_data = base64.b64decode(qr_base64)
        q_image = QImage.fromData(image_data, "PNG")
        pixmap = QPixmap.fromImage(q_image)

        # Display the image in the label
        self.qr_image_label.setPixmap(pixmap.scaled(
            250, 250, Qt.AspectRatioMode.KeepAspectRatio
        ))