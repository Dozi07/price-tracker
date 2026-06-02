from models.product import Product
from sqlalchemy.orm import Session


def create_product(db, product_data: dict):
    db_product = Product(
        name=product_data["name"],
        price=product_data["price"],
        url=product_data["url"],
        image_url=product_data.get("image_url", ""),
        user_id=product_data["user_id"],
        category_id=product_data["category_id"]
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def delete_user_product(db: Session, product_id: int, user_id: int):
    db_product = db.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False