# backend/app/services/qr_service.py

import qrcode
from io import BytesIO
import base64
import json

class QRService:
    @staticmethod
    def generate_session_qr(session_id: str, websocket_url: str) -> str:
        # ... (this function is unchanged)
        qr_data = {
            "type": "session",
            "session_id": session_id,
            "websocket_url": websocket_url
        }
        img = qrcode.make(json.dumps(qr_data))
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return base64_str

    # --- NEW FUNCTION ---
    @staticmethod
    def generate_item_qr(item_qr_code: str) -> str:
        """Generates a QR code for a specific item and returns it as a base64 string."""
        qr_data = {
            "type": "item",
            "qr_code": item_qr_code
        }
        img = qrcode.make(json.dumps(qr_data))
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return base64_str