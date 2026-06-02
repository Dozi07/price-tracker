from typing import List
from pydantic import BaseModel
from schemas.product import ProductOut

class CategoryCreate(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str
    products: List[ProductOut] = []

    class Config:
        from_attributes = True