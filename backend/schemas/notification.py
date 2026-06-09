from datetime import datetime
from pydantic import BaseModel

class NotificationBase(BaseModel):
    product_name: str
    category_name: str
    text: str

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationOut(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True