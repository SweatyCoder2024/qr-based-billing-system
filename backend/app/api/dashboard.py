# backend/app/api/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date

# Corrected imports to be more specific
from ..schemas import dashboard as dashboard_schema
from ..models import order as order_model
from ..models import item as item_model
from ..database import get_db

router = APIRouter()

@router.get("/stats", response_model=dashboard_schema.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Calculate total revenue for today
    today_revenue = db.query(func.sum(order_model.Order.total_amount)).filter(
        func.date(order_model.Order.created_at) == date.today(),
        order_model.Order.status == 'completed'
    ).scalar() or 0.0

    # Calculate total orders for today
    today_orders = db.query(func.count(order_model.Order.id)).filter(
        func.date(order_model.Order.created_at) == date.today()
    ).scalar() or 0

    # Find top 5 selling items
    top_sellers_query = db.query(
        item_model.Item.name,
        func.sum(order_model.OrderItem.quantity).label('quantity_sold'),
        func.sum(order_model.OrderItem.quantity * order_model.OrderItem.unit_price).label('total_revenue')
    ).join(order_model.OrderItem, item_model.Item.id == order_model.OrderItem.item_id)\
     .group_by(item_model.Item.name)\
     .order_by(desc('quantity_sold'))\
     .limit(5).all()

    top_sellers = [
        dashboard_schema.TopSeller(name=name, quantity_sold=qs, total_revenue=tr)
        for name, qs, tr in top_sellers_query
    ]

    return dashboard_schema.DashboardStats(
        total_revenue=today_revenue,
        total_orders=today_orders,
        top_sellers=top_sellers
    )