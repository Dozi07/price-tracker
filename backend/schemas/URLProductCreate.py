from pydantic import BaseModel, HttpUrl

class URLProductCreate(BaseModel):
    url: HttpUrl
    category_id: int