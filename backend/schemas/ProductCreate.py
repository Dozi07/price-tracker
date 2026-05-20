from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: int
    url: str
    user_id : int
