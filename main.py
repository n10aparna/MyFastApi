from fastapi import FastAPI, Depends, HTTPException
from models import Product
from fastapi.middleware.cors import CORSMiddleware
from database import session, engine
import database_models
from sqlalchemy.orm import Session

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# for croos origin resource sharing error
app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)


@app.get("/")
def greet():
    return {"message": "Hello, Family!"}

products = [
    Product(id=101, name="Product 1", price=10.99, description="Description of Product 1", quantity=100),
    Product(id=102, name="Product 2", price=19.99, description="Description of Product 2", quantity=50),
    Product(id=103, name="Product 3", price=5.99, description="Description of Product 3", quantity=200)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    for product in products:
        count = db.query(database_models.Product).count()
        # print(count)
        if count == 0:
            db.add(database_models.Product(**product.model_dump()))
    db.commit()

init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.post("/product")
def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product.id).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists")

    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/product/{product_id}")
def update_product(product_id: int, updated_product: Product, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        # db_product.id = updated_product.id
        db_product.name = updated_product.name
        db_product.price = updated_product.price    
        db_product.description = updated_product.description
        db_product.quantity = updated_product.quantity
        db.commit()
    return {"message": "Product updated successfully", "product": updated_product}


@app.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        db.delete(db_product)
        db.commit()
    return {"message": "Product deleted successfully"}
