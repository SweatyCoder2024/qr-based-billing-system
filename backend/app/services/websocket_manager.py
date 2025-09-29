# backend/app/services/websocket_manager.py

from fastapi import WebSocket
import json
from typing import Dict

class WebSocketManager:
    def __init__(self):
        # A dictionary to hold active connections, with session_id as the key
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
            await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        # (We will build this out later to send messages to all clients)
        pass