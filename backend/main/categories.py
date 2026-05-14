from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from main.get_db import get_db
from main.get_curent_user import get_current_user

from schemas.CategoryCreate import CategoryCreate
from schemas.CategoryOut import CategoryOut
# Импортируем наши новые функции
from crud.category import create_user_category, get_categories_by_user

router = APIRouter()

@router.post("/categories", response_model=CategoryOut)
def add_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_user_category(db, category, current_user.id)

@router.get("/categories", response_model=list[CategoryOut])
def read_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_categories_by_user(db, current_user.id)