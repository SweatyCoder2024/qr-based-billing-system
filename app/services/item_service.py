# backend/app/services/item_service.py

import pandas as pd
import io
from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils.barcode_generator import generate_unique_barcode

def sync_items_from_file(db: Session, file_content: bytes):
    df = pd.read_excel(io.BytesIO(file_content), skiprows=3)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('.', '')

    items_created = 0
    items_updated = 0

    for row in df.itertuples(index=False):
        # --- DATA CLEANING ---
        # Get the values from the row, converting any 'NaN' to None
        qr_code = str(row.barcodeno) if hasattr(row, 'barcodeno') and pd.notna(row.barcodeno) else None

        # If qr_code is missing from file, generate a new one
        if not qr_code:
            qr_code = generate_unique_barcode()

        # Clean up numeric fields that might be empty (NaN)
        mrp = getattr(row, 'mrp', 0.0)
        retail_price = 0.0 if pd.isna(mrp) else mrp

        whole_sale = getattr(row, 'whole_sale', None)
        wholesale_price = None if pd.isna(whole_sale) else whole_sale

        buying_price = getattr(row, 'buying_price', None)
        purchase_rate = None if pd.isna(buying_price) else buying_price

        # Create the data object for validation
        item_data = schemas.item.ItemCreate(
            name=getattr(row, 'product_name', 'N/A'),
            retail_price=retail_price,
            wholesale_price=wholesale_price,
            qr_code=qr_code,
            stock_quantity=getattr(row, 'stock', 0),
            category=getattr(row, 'category_name', None),
            purchase_rate=purchase_rate,
            tax_percent=getattr(row, 'tax%', 0.0),
            hsn_code=str(getattr(row, 'hsn_code', '')) if hasattr(row, 'hsn_code') else None,
            unit=getattr(row, 'unit', None),
            reorder_stock=getattr(row, 'reorder_stock', 0),
            supplier_name=getattr(row, 'supplier_name', None)
        )

        # Find existing item to update, or create a new one
        db_item = db.query(models.item.Item).filter(models.item.Item.qr_code == item_data.qr_code).first()

        if db_item:
            for key, value in item_data.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            items_updated += 1
        else:
            db_item = models.item.Item(**item_data.model_dump())
            db.add(db_item)
            items_created += 1

    db.commit()
    return {"created": items_created, "updated": items_updated}