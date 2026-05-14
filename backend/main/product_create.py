from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.URLProductCreate import URLProductCreate
from schemas.ProductOut import ProductOut
from main.get_db import get_db
from main.get_curent_user import get_current_user
from crud.product_create import create_product
from parcer.ozon_parcer import parse_ozon_product

router = APIRouter()


@router.post("/add_product", response_model=ProductOut)
def add_product(product: URLProductCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    url_str = str(product.url)

    print("Начинаем парсинг товара")
    parsed_data = parse_ozon_product(url_str)
    print(f"Парсинг завершен: {parsed_data}")

    #данные для базы
    product_dict = {
        "name": parsed_data["name"],
        "price": parsed_data["price"],
        "url": url_str,
        "user_id": current_user.id,
        "category_id": product.category_id
    }

    #cохраняем в БД
    return create_product(db, product_dict)