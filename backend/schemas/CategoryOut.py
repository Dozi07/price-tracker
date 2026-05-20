from pydantic import BaseModel
from typing import List
from schemas.ProductOut import ProductOut

class CategoryOut(BaseModel):
    id: int
    name: str
    products: List[ProductOut] = []

    class Config:
        from_attributes = True