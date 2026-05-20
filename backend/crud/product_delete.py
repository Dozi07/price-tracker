from sqlalchemy.orm import Session
from models.Product import Product


def delete_user_product(db: Session, product_id: int, user_id: int):
    db_product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False