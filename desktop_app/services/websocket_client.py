# desktop_app/services/websocket_client.py

import asyncio
import websockets
import json
from typing import Callable, Optional

class WebSocketClient:
    def __init__(self):
        self.connection: Optional[websockets.WebSocketClientProtocol] = None
        self.message_handler: Optional[Callable[[dict], None]] = None
        self._is_running = False

    def set_message_handler(self, handler: Callable[[dict], None]):
        self.message_handler = handler

    async def connect_and_listen(self, session_id: str, base_ws_url: str = "ws://localhost:8000"):
        uri = f"{base_ws_url}/ws/{session_id}"
        self._is_running = True
        try:
            async with websockets.connect(uri, ping_interval=20, ping_timeout=20) as websocket:
                self.connection = websocket
                print(f"WebSocket connected to {uri}")
                while self._is_running:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        print(f"--- DESKTOP RECEIVED MESSAGE ---: {message}")
                        data = json.loads(message)
                        if self.message_handler:
                            self.message_handler(data)
                    except asyncio.TimeoutError:
                        continue
        except (asyncio.CancelledError, websockets.exceptions.ConnectionClosed) as e:
            print(f"WebSocket connection closed cleanly: {type(e).__name__}")
        except Exception as e:
            print(f"WebSocket connection error: {e}")
        finally:
            self.connection = None
            self._is_running = False

    def stop(self):
        self._is_running = False