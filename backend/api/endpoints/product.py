from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.dependencies import get_db, get_current_user
from schemas.product import ProductOut, URLProductCreate
from models.product import Product, ProductPriceHistory
from crud.product import create_product, delete_user_product
from services.parser.ozon import parse_ozon_product
from services.parser.wb import parse_wb_product
from services.parser.market import parse_yandex_market_product

router = APIRouter(tags=["Products"])


@router.post("/add_product", response_model=ProductOut)
def add_product(
        product: URLProductCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    url_str = str(product.url)


    print(f"Начинаем парсинг товара. ID маркетплейса: {product.marketplace_id}")

    if product.marketplace_id == 1:
        parsed_data = parse_ozon_product(url_str)
    elif product.marketplace_id == 2:
        parsed_data = parse_wb_product(url_str)
    elif product.marketplace_id == 3:
        parsed_data = parse_yandex_market_product(url_str)
    else:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неподдерживаемый маркетплейс. Допустимые значения: 1 (Ozon), 2 (WB), 3 (Yandex Market)"
        )

    print(f"Парсинг завершен: {parsed_data}")


    if not parsed_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось получить данные о товаре. Проверьте ссылку."
        )

    product_dict = {
        "name": parsed_data.get("name", "Без названия"),
        "price": parsed_data.get("price", 0),
        "image_url": parsed_data.get("image_url", ""),
        "url": url_str,
        "user_id": current_user.id,
        "category_id": product.category_id
    }

    created_product = create_product(db, product_dict)

    new_history = ProductPriceHistory(
        product_id=created_product.id,
        price=created_product.price,
        date=date.today()
    )

    db.add(new_history)
    db.commit()
    db.refresh(created_product)

    return {
        "id": created_product.id,
        "name": created_product.name,
        "price": created_product.price,
        "image_url": created_product.image_url,
        "url": created_product.url,
        "category_id": created_product.category_id,
        "min_price": created_product.price,
        "max_price": created_product.price
    }
@router.get("/products", response_model=List[ProductOut])
async def get_user_products(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    products = db.query(Product).filter(Product.user_id == current_user.id).all()

    if not products:
        return []

    return products

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    success = delete_user_product(db, product_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден или у вас нет прав на его удаление"
        )

    return {"detail": "Товар успешно удален"}