# backend/app/api/sessions.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import uuid

from ..schemas import session as session_schema
from ..models import session as session_model
from ..database import get_db
from ..services.qr_service import QRService

router = APIRouter()

# !!! IMPORTANT: REPLACE THIS WITH YOUR NEW LAPTOP'S IP ADDRESS !!!
HOST_IP_ADDRESS = "192.168.0.231" # e.g., "192.168.1.15"

@router.post("/create", response_model=session_schema.SessionResponse)
def create_session(request: Request, db: Session = Depends(get_db)):
    new_session_id = f"SESS-{uuid.uuid4().hex[:8].upper()}"

    db_session = session_model.DesktopSession(session_id=new_session_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    websocket_url = f"ws://{HOST_IP_ADDRESS}:8000/ws/{db_session.session_id}"

    qr_code_str = QRService.generate_session_qr(
        session_id=db_session.session_id,
        websocket_url=websocket_url
    )

    response_data = db_session.__dict__
    response_data['qr_code'] = qr_code_str

    return response_data