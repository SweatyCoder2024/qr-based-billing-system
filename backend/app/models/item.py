# backend/app/models/item.py

from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, func
from ..database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    retail_price = Column(DECIMAL(10, 2), nullable=False)
    wholesale_price = Column(DECIMAL(10, 2), nullable=True)
    qr_code = Column(String(255), unique=True, nullable=False, index=True)
    stock_quantity = Column(Integer, default=0)
    category = Column(String(100), index=True)
    tax_percent = Column(DECIMAL(5, 2), default=0.0)
    purchase_rate = Column(DECIMAL(10, 2), nullable=True)
    hsn_code = Column(String(50), nullable=True)
    unit = Column(String(50), nullable=True)
    reorder_stock = Column(Integer, default=0, nullable=True)
    supplier_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())