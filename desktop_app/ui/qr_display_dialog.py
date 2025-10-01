# desktop_app/ui/qr_display_dialog.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import base64

class QRDisplayDialog(QDialog):
    def __init__(self, item_name: str, qr_base64: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"QR Code for: {item_name}")

        layout = QVBoxLayout(self)

        image_label = QLabel()

        # Decode the base64 string into an image
        image_data = base64.b64decode(qr_base64)
        q_image = QImage.fromData(image_data, "PNG")
        pixmap = QPixmap.fromImage(q_image)

        image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(image_label)