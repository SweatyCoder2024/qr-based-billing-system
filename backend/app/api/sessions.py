# backend/app/api/sessions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

# The import alias is 'session_schema'
from ..schemas import session as session_schema
from ..models import session as session_model
from ..database import get_db
from ..services.qr_service import QRService

router = APIRouter()

# NOTE: Ensure this is set to your laptop's IP address
HOST_IP_ADDRESS = "192.168.0.231" 

def get_qr_for_session(session: session_model.DesktopSession) -> str:
    """Helper function to generate a QR code for a given session object."""
    websocket_url = f"ws://{HOST_IP_ADDRESS}:8000/ws/{session.session_id}"
    return QRService.generate_session_qr(
        session_id=session.session_id,
        websocket_url=websocket_url
    )

@router.post("/create", response_model=session_schema.SessionResponse, tags=["Sessions"])
def create_session(db: Session = Depends(get_db)):
    """Creates a new, active session and returns its details including a QR code."""
    new_session_id = f"SESS-{uuid.uuid4().hex[:8].upper()}"

    db_session = session_model.DesktopSession(session_id=new_session_id, is_active=True)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    qr_code_str = get_qr_for_session(db_session)

    return {
        "id": db_session.id,
        "session_id": db_session.session_id,
        "is_active": db_session.is_active,
        "created_at": db_session.created_at,
        "expires_at": db_session.expires_at,
        "qr_code": qr_code_str
    }

# --- THIS IS THE CORRECTED LINE ---
@router.get("/active", response_model=List[session_schema.DesktopSession], tags=["Sessions"])
def get_active_sessions(db: Session = Depends(get_db)):
    """Returns a list of all currently active sessions."""
    active_sessions = db.query(session_model.DesktopSession).filter(session_model.DesktopSession.is_active == True).all()
    return active_sessions

@router.get("/{session_id}/qr", response_model=session_schema.SessionResponse, tags=["Sessions"])
def get_session_qr(session_id: str, db: Session = Depends(get_db)):
    """Gets the details and QR code for a specific existing session."""
    db_session = db.query(session_model.DesktopSession).filter(session_model.DesktopSession.session_id == session_id).first()

    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    qr_code_str = get_qr_for_session(db_session)

    return {
        "id": db_session.id,
        "session_id": db_session.session_id,
        "is_active": db_session.is_active,
        "created_at": db_session.created_at,
        "expires_at": db_session.expires_at,
        "qr_code": qr_code_str
    }