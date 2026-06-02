from pydantic import BaseModel

class ProductOut(BaseModel):
    id : int
    name : str
    price : int
    url : str
    category_id: int
    image_url: str
    min_price: int
    max_price: int

    class Config:
        from_attributes = True
        