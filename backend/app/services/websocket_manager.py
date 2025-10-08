# backend/app/services/websocket_manager.py

from fastapi import WebSocket
from sqlalchemy.orm import Session
import json
from typing import Dict, List
from datetime import datetime
import decimal

from ..database import SessionLocal
from ..services import order_service
from ..schemas.order import Order as OrderSchema

def json_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        return str(o)

class WebSocketManager:
    def __init__(self):
        # This now stores a LIST of websockets for each session ID
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        # Add the new connection to the list for this session
        self.active_connections[session_id].append(websocket)
        print(f"WebSocket connected for session: {session_id}. Total clients: {len(self.active_connections[session_id])}")

    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            # Remove the specific websocket from the list
            self.active_connections[session_id].remove(websocket)
            print(f"WebSocket disconnected for session: {session_id}. Remaining clients: {len(self.active_connections[session_id])}")
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast_to_session(self, message: dict, session_id: str):
        """Sends a message to ALL clients connected to a specific session."""
        if session_id in self.active_connections:
            message_str = json.dumps(message, default=json_converter)
            # Iterate over all websockets in the list and send the message
            for connection in self.active_connections[session_id]:
                await connection.send_text(message_str)

    async def handle_message(self, session_id: str, data: str):
        db: Session = SessionLocal()
        try:
            message = json.loads(data)
            message_type = message.get("type")

            if message_type == "item_scanned":
                item_qr_code = message.get("data", {}).get("qr_code")
                if item_qr_code:
                    print(f"Received item_scanned for {item_qr_code} in session {session_id}")
                    updated_order = order_service.add_item_to_order(session_id, item_qr_code, db)
                    order_data = OrderSchema.from_orm(updated_order).model_dump()
                    await self.broadcast_to_session({
                        "type": "order_update",
                        "data": order_data
                    }, session_id)

            # --- NEW LOGIC TO HANDLE CREATING A BILL ---
            elif message_type == "create_new_bill":
                print(f"Received create_new_bill for session {session_id}")
                new_order = order_service.create_order_for_session(session_id, db)

                # Broadcast a message so the desktop knows a new bill was created
                # For now, we'll just re-use the order_update message type
                order_data = OrderSchema.from_orm(new_order).model_dump()
                await self.broadcast_to_session({
                    "type": "order_update", 
                    "data": order_data
                }, session_id)

            else:
                await self.broadcast_to_session({"error": "Unknown message type"}, session_id)

        except Exception as e:
            print(f"Error handling message: {e}")
            await self.broadcast_to_session({"type": "error", "message": str(e)}, session_id)
        finally:
            db.close()