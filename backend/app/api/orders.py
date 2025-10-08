# backend/app/api/orders.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import List

from ..database import get_db
from ..services import pdf_service
from .. import models
from ..schemas import order as order_schema

router = APIRouter()

@router.get("/session/{session_id}", response_model=order_schema.Order, tags=["Orders"])
def get_order_by_session(session_id: str, db: Session = Depends(get_db)):
    """
    Fetches the pending order associated with a given session ID.
    """
    desktop_session = db.query(models.session.DesktopSession).filter(models.session.DesktopSession.session_id == session_id).first()
    if not desktop_session:
        raise HTTPException(status_code=404, detail="Session not found")

    order = db.query(models.order.Order).options(
        joinedload(models.order.Order.items).joinedload(models.order.OrderItem.item)
    ).filter(
        models.order.Order.session_id == desktop_session.id,
        models.order.Order.status == 'pending'
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="No pending order found for this session")
        
    return order

@router.get("/{order_id}/pdf", tags=["Orders"])
def generate_order_bill(order_id: int, db: Session = Depends(get_db)):
    """
    Fetches an order by its ID and generates a PDF bill for it.
    """
    order = db.query(models.order.Order).options(
        joinedload(models.order.Order.items).joinedload(models.order.OrderItem.item)
    ).filter(models.order.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order_details = {
        "id": order.id,
        "date": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "items": [
            {
                "name": oi.item.name,
                "quantity": oi.quantity,
                "unit_price": float(oi.unit_price),
                "total_price": float(oi.quantity * oi.unit_price)
            } for oi in order.items
        ],
        "total_amount": float(order.total_amount)
    }

    pdf_bytes = pdf_service.generate_bill_pdf(order_details)

    return Response(
        content=pdf_bytes,
        media_type='application/pdf',
        headers={"Content-Disposition": f"attachment; filename=order_{order_id}_bill.pdf"}
    )