# backend/app/schemas/order.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import decimal
from .item import Item as ItemSchema # Import the existing Item schema

class OrderItemBase(BaseModel):
    quantity: int
    unit_price: decimal.Decimal

class OrderItem(OrderItemBase):
    id: int
    item: ItemSchema # Nest the full item details

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    status: str
    total_amount: decimal.Decimal

class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        from_attributes = True