from sqlalchemy.orm import Session
from models.Category import Category
from schemas.CategoryCreate import CategoryCreate

def create_user_category(db: Session, category: CategoryCreate, user_id: int):
    #создание новой категории
    db_category = Category(name=category.name, user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories_by_user(db: Session, user_id: int):
    #получаем все категории пользователя
    return db.query(Category).filter(Category.user_id == user_id).all()

def get_category_by_id(db: Session, category_id: int, user_id: int):
    #находим конкретную категорию
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()