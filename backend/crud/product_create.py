from sqlalchemy.orm import Session
from models.Product import Product

from models.Users import User

#def create_product(db: Session, product_data: dict):
#   new_product = Product(**product_data)
#    db.add(new_product)
#    db.commit()
#    db.refresh(new_product)
#    return new_product

from models.Product import Product


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
