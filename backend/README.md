# QR Billing System - Backend

This repository contains the backend server for the QR-based Billing System. It is a robust API built with FastAPI that handles item management, database interactions, real-time communication, and more.

## Current Status
The backend foundation for **Item Management** is complete and fully functional.

---

## Features Implemented So Far
- **Dockerized Environment:** The entire application and database run in Docker containers for consistency and ease of deployment.
- **PostgreSQL Database:** Uses a robust PostgreSQL database for data storage.
- **Database Migrations:** Uses Alembic to safely manage changes to the database schema over time.
- **Full Item CRUD API:** A complete set of API endpoints to Create, Read, Update, and Delete items.
- **Advanced File Upload:** An endpoint to bulk-upload items from both `.csv` and `.xlsx` files.
- **Automatic Barcode Generation:** The system automatically generates unique `ITEM-XXXXXXXX` style barcodes for products that don't have one in the upload file.
- **Dual Pricing Model:** The database and API support both `retail_price` and `wholesale_price` for each item.

---

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Containerization:** Docker & Docker Compose
- **Data Validation:** Pydantic
- **Database ORM:** SQLAlchemy
- **Migrations:** Alembic
- **File Parsing:** Pandas & OpenPyXL

---

## How to Run
1.  Ensure Docker Desktop is running.
2.  Navigate to the `backend` directory in your terminal.
3.  Run `docker-compose down` to ensure a clean slate.
4.  Run `docker-compose up --build` to build the images and start the services.
5.  The API will be available at `http://localhost:8000`.
6.  Interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.