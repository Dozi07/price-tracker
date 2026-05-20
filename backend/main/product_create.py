from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from schemas.URLProductCreate import URLProductCreate
from schemas.ProductOut import ProductOut
from main.get_db import get_db
from main.get_curent_user import get_current_user
from crud.product_create import create_product
from crud.product_delete import delete_user_product
from crud.category import delete_category  
from parcer.ozon_parcer import parse_ozon_product
from models.ProductPriceHistory import ProductPriceHistory
from models.Product import Product
router = APIRouter()


@router.post("/add_product", response_model=ProductOut)
def add_product(
    product: URLProductCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    url_str = str(product.url)

    print("Начинаем парсинг товара")
    parsed_data = parse_ozon_product(url_str)
    print(f"Парсинг завершен: {parsed_data}")


    product_dict = {
        "name": parsed_data["name"],
        "price": parsed_data["price"],
        "url": url_str,
        "user_id": current_user.id,
        "category_id": product.category_id
    }
    created_product = create_product(db, product_dict)
    #return create_product(db, product_dict)
    new_history = ProductPriceHistory(product_id=created_product.id, price=created_product.price, date=date.today()
    )
    db.add(new_history)
    db.commit()
    return {
        "id": created_product.id,
        "name": created_product.name,
        "price": created_product.price,
        "url": created_product.url,
        "category_id": created_product.category_id,
        "min_price": created_product.price,
        "max_price": created_product.price
    }

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = delete_user_product(db, product_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден или у вас нет прав на его удаление"
        )
    
    return {"detail": "Товар успешно удален"}