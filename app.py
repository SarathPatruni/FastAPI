from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
import database_models
from session_maker import engine
from session_maker import session
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)



database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome to Sarath WareHouse"

products = [
    Product(id= 1, name= "Washing Machine", description= "A washing Machine", price= 20000, quantity= 1),
    Product(id= 2, name= "Refrigerator", description= "A fridge", price= 25000, quantity= 1),
    Product(id= 3, name= "LED TV", description= "A Telivsion", price= 40000, quantity= 1),
    Product(id= 4, name= "Phone", description= "Poco X5 Pro", price= 25000, quantity= 1),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()

init_db()

@app.get("/products")
def get_all_product(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        return db_products 
    return "Product Not Found"

@app.post("/products")
def add_a_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_a_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        db_products.name = product.name
        db_products.description = product.description
        db_products.price = product.price
        db_products.quantity = product.quantity
        db.commit()
        db.refresh(db_products)
        return db_products
    else:
        return "Product Not Found"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return "Product Deleted Successfully"
    else:
        return "Product Not Found"

