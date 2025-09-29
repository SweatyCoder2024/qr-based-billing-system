# backend/app/api/items.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schemas import item as item_schema
from ..models import item as item_model
from ..database import get_db
from ..services import item_service

router = APIRouter()

@router.post("/", response_model=item_schema.Item)
def create_item(item: item_schema.ItemCreate, db: Session = Depends(get_db)):
    # ... (this function remains the same)
    db_item = db.query(item_model.Item).filter(item_model.Item.qr_code == item.qr_code).first()
    if db_item:
        raise HTTPException(status_code=409, detail="Item with this QR code already exists")
    new_item = item_model.Item(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[item_schema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # ... (this function remains the same)
    items = db.query(item_model.Item).offset(skip).limit(limit).all()
    return items

@router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # ... (this function remains the same)
    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV or XLSX file.")
    file_content = await file.read()
    try:
        result = item_service.sync_items_from_file(db, file_content)
        return {"message": "File processed successfully", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

# --- NEW FUNCTION: GET A SINGLE ITEM ---
@router.get("/{item_id}", response_model=item_schema.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# --- NEW FUNCTION: UPDATE AN ITEM ---
@router.put("/{item_id}", response_model=item_schema.Item)
def update_item(item_id: int, item: item_schema.ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- NEW FUNCTION: DELETE AN ITEM ---
@router.delete("/{item_id}", response_model=item_schema.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return db_item