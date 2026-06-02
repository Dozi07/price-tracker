from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.Creating_eng_db import Base
from models.ProductPriceHistory import ProductPriceHistory

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_url = Column(String, nullable=True)

    category_id = Column(Integer, ForeignKey("category.id"))

    category = relationship("Category", back_populates="products")

    price_history = relationship("ProductPriceHistory", back_populates="product", cascade="all, delete-orphan")