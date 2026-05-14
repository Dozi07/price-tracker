from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from main.get_db import get_db
from models.Product import Product
from main.get_curent_user import get_current_user
from schemas.ProductOut import ProductOut
router = APIRouter(tags=["Products"])


@router.get("/products", response_model=List[ProductOut])
async def get_user_products(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):

    products = db.query(Product).filter(Product.owner_id == current_user.id).all()

    if not products:
        return []

    return products