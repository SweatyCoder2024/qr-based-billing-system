# backend/app/schemas/session.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DesktopSessionBase(BaseModel):
    session_id: str
    is_active: bool = True

class DesktopSessionCreate(BaseModel):
    pass # No data needed to create a session

class DesktopSession(DesktopSessionBase):
    id: int
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SessionResponse(DesktopSession):
    qr_code: str # Add qr_code field for the response