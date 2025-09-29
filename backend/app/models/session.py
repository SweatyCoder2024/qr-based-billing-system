# backend/app/models/session.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class DesktopSession(Base):
    __tablename__ = "desktop_sessions"

    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), unique=True, index=True) # The public-facing session ID
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship("Order", back_populates="session")