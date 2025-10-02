# backend/app/services/order_service.py

from sqlalchemy.orm import Session
from .. import models
from ..schemas import order as order_schema # <-- Corrected import

def add_item_to_order(session_id: str, item_qr_code: str, db: Session) -> order_schema.Order: # <-- Use corrected schema
    # 1. Find the item in the database from its QR code
    item = db.query(models.item.Item).filter(models.item.Item.qr_code == item_qr_code).first()
    if not item:
        raise ValueError(f"Item with QR code {item_qr_code} not found.")

    # 2. Find the desktop session
    desktop_session = db.query(models.session.DesktopSession).filter(models.session.DesktopSession.session_id == session_id).first()
    if not desktop_session:
        raise ValueError(f"Session {session_id} not found.")

    # 3. Find an active (pending) order for this session, or create one
    order = db.query(models.order.Order).filter(
        models.order.Order.session_id == desktop_session.id,
        models.order.Order.status == 'pending'
    ).first()

    if not order:
        order = models.order.Order(session_id=desktop_session.id, status='pending')
        db.add(order)
        db.flush() 

    # 4. Check if the item is already in the order
    order_item = db.query(models.order.OrderItem).filter(
        models.order.OrderItem.order_id == order.id,
        models.order.OrderItem.item_id == item.id
    ).first()

    if order_item:
        # If it exists, just increase the quantity
        order_item.quantity += 1
    else:
        # If not, create a new order_item entry
        order_item = models.order.OrderItem(
            order_id=order.id,
            item_id=item.id,
            quantity=1,
            unit_price=item.retail_price
        )
        db.add(order_item)

    # 5. Recalculate the order's total amount
    # We need to commit to get the latest order.items relationship
    db.commit()
    db.refresh(order)
    total = sum(oi.quantity * oi.unit_price for oi in order.items)
    order.total_amount = total

    db.commit()
    db.refresh(order)

    # 6. Return the updated order data
    return order