from pydantic import BaseModel, HttpUrl

class ProductCreate(BaseModel):
    name: str
    price: int
    url: str
    image_url: str
    user_id: int


class ProductOut(BaseModel):
    id: int
    name: str
    price: int
    url: str
    category_id: int
    image_url: str
    min_price: int
    max_price: int

    class Config:
        from_attributes = True

class URLProductCreate(BaseModel):
    url: HttpUrl
    category_id: int
    marketplace_id: int
