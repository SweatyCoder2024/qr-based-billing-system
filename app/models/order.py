# backend/app/models/order.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), default='pending') # e.g., pending, completed, cancelled
    total_amount = Column(DECIMAL(10, 2), default=0.0)

    # Foreign Keys to link to other tables
    session_id = Column(Integer, ForeignKey("desktop_sessions.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # This creates a "relationship" so we can easily access all items for an order
    items = relationship("OrderItem", back_populates="order")
    session = relationship("DesktopSession", back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False) # Price at the time of sale

    # Foreign Keys
    order_id = Column(Integer, ForeignKey("orders.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    # Relationships
    order = relationship("Order", back_populates="items")
    item = relationship("Item")