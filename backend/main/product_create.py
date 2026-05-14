from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from main.get_db import get_db
from crud.product_create import create_product
from schemas.ProductOut import ProductOut
from schemas.URLProductCreate import URLProductCreate
from main.get_curent_user import get_current_user

router = APIRouter(tags=["product_create"])

@router.post("/add_product", response_model=ProductOut)
def add_product(url : URLProductCreate,
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)):
    #вызов парсера
    #parsing_product = parsing_ozon что то такое
    #затычка на время
    parsed_data = {
        "name": "Смартфон из парсера",
        "price": 50000.0
    }
    if not parsed_data:
        raise HTTPException(status_code=400, detail="Не удалось спарсить данные по ссылке")

    product_dict = {
        "name": parsed_data["name"],
        "price": parsed_data["price"],
        "url": str(url.url),
        "user_id": current_user.id
    }
    
    return create_product(db, product_dict)