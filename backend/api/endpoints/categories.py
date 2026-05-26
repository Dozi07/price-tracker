from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from api.dependencies import get_db, get_current_user
from models.category import Category
from models.product import ProductPriceHistory
from crud.category import delete_category
from schemas.category import CategoryCreate

router = APIRouter(
    tags=["Categories"]
)

@router.get("/categories")
def get_categories(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    categories = db.query(Category).filter(Category.user_id == current_user.id).all()

    result = []
    for cat in categories:
        products_list = []
        for p in cat.products:
            prices = db.query(
                func.min(ProductPriceHistory.price).label("min_p"),
                func.max(ProductPriceHistory.price).label("max_p")
            ).filter(ProductPriceHistory.product_id == p.id).first()

            min_price = prices.min_p if prices.min_p is not None else p.price
            max_price = prices.max_p if prices.max_p is not None else p.price

            products_list.append({
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "url": p.url,
                "image_url": p.image_url,
                "category_id": p.category_id,
                "min_price": min_price,
                "max_price": max_price
            })

        result.append({
            "id": cat.id,
            "name": cat.name,
            "products": products_list
        })

    return result

@router.post("/categories")
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_cat = Category(name=category.name, user_id=current_user.id)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@router.delete("/categories/{category_id}")
def delete_user_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    success = delete_category(db, category_id=category_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Категория не найдена")