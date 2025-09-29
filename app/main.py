# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import item

# Add this line to import the new items API file
from .api import items

Base.metadata.create_all(bind=engine)

app = FastAPI(title="QR Billing System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add this line to connect the items router to the main app
app.include_router(items.router, prefix="/api/items", tags=["Items"])

@app.get("/")
async def root():
    return {"message": "Welcome to the QR Billing System API"}