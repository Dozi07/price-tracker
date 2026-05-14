from sqlalchemy.orm import Session
from models.Product import Product

from models.Users import User

def create_product(db: Session, product_data: dict):
    new_product = Product(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

