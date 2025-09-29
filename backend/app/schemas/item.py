# backend/app/schemas/item.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import decimal

class ItemBase(BaseModel):
    name: str
    retail_price: decimal.Decimal
    wholesale_price: Optional[decimal.Decimal] = None
    qr_code: Optional[str] = None
    stock_quantity: int = 0
    category: Optional[str] = None
    tax_percent: Optional[decimal.Decimal] = 0.0
    purchase_rate: Optional[decimal.Decimal] = None
    hsn_code: Optional[str] = None
    unit: Optional[str] = None
    reorder_stock: Optional[int] = 0
    supplier_name: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    retail_price: Optional[decimal.Decimal] = None
    wholesale_price: Optional[decimal.Decimal] = None
    stock_quantity: Optional[int] = None
    category: Optional[str] = None
    tax_percent: Optional[decimal.Decimal] = None
    purchase_rate: Optional[decimal.Decimal] = None
    hsn_code: Optional[str] = None
    unit: Optional[str] = None
    reorder_stock: Optional[int] = None
    supplier_name: Optional[str] = None

class Item(ItemBase):
    id: int
    qr_code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True