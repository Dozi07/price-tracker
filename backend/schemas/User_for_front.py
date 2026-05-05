from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User_for_front(BaseModel):
    id: int
    email: EmailStr
