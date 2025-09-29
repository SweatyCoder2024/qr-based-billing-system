# backend/app/api/sessions.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import uuid

from ..schemas import session as session_schema
from ..models import session as session_model
from ..database import get_db
from ..services.qr_service import QRService

router = APIRouter()

@router.post("/create", response_model=session_schema.SessionResponse)
def create_session(request: Request, db: Session = Depends(get_db)):
    # Generate a new unique session ID
    new_session_id = f"SESS-{uuid.uuid4().hex[:8].upper()}"

    # Create a new session object and save it to the database
    db_session = session_model.DesktopSession(session_id=new_session_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    # Define the WebSocket URL the mobile app will connect to
    # We use the request object to get the server's host and port
    websocket_url = f"ws://{request.client.host}:8000/ws/{db_session.session_id}"

    # Generate the QR code
    qr_code_str = QRService.generate_session_qr(
        session_id=db_session.session_id,
        websocket_url=websocket_url
    )

    # Combine the session data and QR code for the response
    response_data = db_session.__dict__
    response_data['qr_code'] = qr_code_str

    return response_data