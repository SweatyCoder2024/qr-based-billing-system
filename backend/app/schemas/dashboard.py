# backend/app/schemas/dashboard.py

from pydantic import BaseModel
from typing import List, Optional
import decimal

class TopSeller(BaseModel):
    name: str
    quantity_sold: int
    total_revenue: decimal.Decimal

class DashboardStats(BaseModel):
    total_revenue: decimal.Decimal
    total_orders: int
    top_sellers: List[TopSeller]