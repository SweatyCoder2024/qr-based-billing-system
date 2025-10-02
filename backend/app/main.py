# backend/app/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import item, order, session
from .api import items, sessions, dashboard, orders # <-- ADD orders here
from .services.websocket_manager import WebSocketManager

Base.metadata.create_all(bind=engine)

app = FastAPI(title="QR Billing System API", version="1.0.0")

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
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"]) # <-- ADD THIS LINE

@app.get("/")
async def root():
    return {"message": "Welcome to the QR Billing System API"}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket_manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            # The manager now handles getting its own DB session
            await websocket_manager.handle_message(session_id, data)
    except WebSocketDisconnect:
        websocket_manager.disconnect(session_id)
