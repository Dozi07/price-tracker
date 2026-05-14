from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: str
    url: str
    user_id : int
