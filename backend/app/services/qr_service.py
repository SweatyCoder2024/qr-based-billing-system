# backend/app/services/qr_service.py

import qrcode
from io import BytesIO
import base64
import json

class QRService:
    @staticmethod
    def generate_session_qr(session_id: str, websocket_url: str) -> str:
        """Generates a QR code for desktop-mobile connection and returns it as a base64 string."""
        qr_data = {
            "type": "session",
            "session_id": session_id,
            "websocket_url": websocket_url
        }

        img = qrcode.make(json.dumps(qr_data))

        buffer = BytesIO()
        img.save(buffer, format="PNG")

        # Encode the image bytes to a base64 string to send via JSON
        base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return base64_str