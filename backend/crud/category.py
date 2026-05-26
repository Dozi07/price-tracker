from sqlalchemy.orm import Session
from models.category import Category
from models.product import Product, ProductPriceHistory
from schemas.category import CategoryCreate


def create_user_category(db: Session, category: CategoryCreate, user_id: int):
    db_category = Category(name=category.name, user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories_by_user(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()

def get_category_by_id(db: Session, category_id: int, user_id: int):
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
def delete_category(db: Session, category_id: int, user_id: int):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    
    if not category:
        return False

    product_ids = [p.id for p in category.products]
    
    if product_ids:
        db.query(ProductPriceHistory).filter(ProductPriceHistory.product_id.in_(product_ids)).delete(synchronize_session=False)
        db.query(Product).filter(Product.id.in_(product_ids)).delete(synchronize_session=False)

    db.delete(category)
    db.commit()
    return True