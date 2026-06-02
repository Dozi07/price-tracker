from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User_for_front(BaseModel):
    id: int
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None