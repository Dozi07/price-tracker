from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel): # Создаем класс который показывает в каком формате приходят данные
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: str
    class Config:

        from_attributes = True