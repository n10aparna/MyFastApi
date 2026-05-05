# MyFastApi

A FastAPI application for managing products with CRUD operations using SQLAlchemy and PostgreSQL.

## Installation

- Install required packages: `pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic`

## Database Setup

- Ensure PostgreSQL is running and update the database URL in `database.py` if needed.

## Running the Application

- Run `uvicorn main:app --reload`

## API Endpoints

- `GET /`: Greeting message
- `GET /products`: Retrieve all products
- `GET /product/{product_id}`: Retrieve a specific product
- `POST /product`: Create a new product
- `PUT /product/{product_id}`: Update an existing product
- `DELETE /product/{product_id}`: Delete a product