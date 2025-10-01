# backend/app/api/orders.py

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..services import pdf_service

router = APIRouter()

@router.post("/generate-test-bill", tags=["Orders"])
def generate_test_bill(db: Session = Depends(get_db)):
    # Create fake order data for testing purposes
    test_order_details = {
        "id": 101,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": [
            {"name": "Parle-G Biscuit", "quantity": 2, "unit_price": 10.00, "total_price": 20.00},
            {"name": "Surf Excel 1kg", "quantity": 1, "unit_price": 220.00, "total_price": 220.00},
            {"name": "KitKat", "quantity": 5, "unit_price": 25.00, "total_price": 125.00},
        ],
        "total_amount": 365.00
    }

    # Call our service to generate the PDF bytes
    pdf_bytes = pdf_service.generate_bill_pdf(test_order_details)

    # Return the PDF as a response
    return Response(
        content=pdf_bytes,
        media_type='application/pdf',
        headers={"Content-Disposition": "attachment; filename=bill.pdf"}
    )