# backend/app/services/websocket_manager.py

from fastapi import WebSocket, Depends
from sqlalchemy.orm import Session
import json
from typing import Dict
from ..database import SessionLocal
from ..services import order_service
from ..schemas.order import Order as OrderSchema

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        print(f"WebSocket connected for session: {session_id}")

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            print(f"WebSocket disconnected for session: {session_id}")

    async def send_personal_message(self, message: dict, session_id: str):
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            await websocket.send_text(json.dumps(message, default=str)) # Use default=str to handle Decimals/DateTimes

    async def handle_message(self, session_id: str, data: str):
        db: Session = SessionLocal()
        try:
            message = json.loads(data)
            message_type = message.get("type")

            if message_type == "item_scanned":
                item_qr_code = message.get("data", {}).get("qr_code")
                if item_qr_code:
                    print(f"Received item_scanned for {item_qr_code} in session {session_id}")
                    # Call the order service
                    updated_order = order_service.add_item_to_order(session_id, item_qr_code, db)

                    # Broadcast the updated order back to the client
                    order_data = OrderSchema.from_orm(updated_order).dict()
                    await self.send_personal_message({
                        "type": "order_update",
                        "data": order_data
                    }, session_id)
            else:
                await self.send_personal_message({"error": "Unknown message type"}, session_id)

        except Exception as e:
            print(f"Error handling message: {e}")
            await self.send_personal_message({"type": "error", "message": str(e)}, session_id)
        finally:
            db.close()