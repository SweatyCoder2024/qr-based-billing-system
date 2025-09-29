# backend/app/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import item, order, session
from .api import items, sessions
from .services.websocket_manager import WebSocketManager # <-- ADD THIS IMPORT

Base.metadata.create_all(bind=engine)

app = FastAPI(title="QR Billing System API", version="1.0.0")

# Create an instance of our manager
websocket_manager = WebSocketManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router, prefix="/api/items", tags=["Items"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])

@app.get("/")
async def root():
    return {"message": "Welcome to the QR Billing System API"}

# --- NEW WEBSOCKET ENDPOINT ---
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket_manager.connect(websocket, session_id)
    try:
        while True:
            # The server will wait here to receive messages from a client
            data = await websocket.receive_text()
            # (We will add logic later to handle incoming messages)
            await websocket_manager.send_personal_message(
                {"message": f"Message received: {data}"}, session_id
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(session_id)