from pydantic import BaseModel

class ProductOut(BaseModel):
    id : int
    name : str
    price : str
    url : str