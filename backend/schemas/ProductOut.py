from pydantic import BaseModel

class ProductOut(BaseModel):
    id : int
    name : str
    price : int
    url : str
    url_picture: str
