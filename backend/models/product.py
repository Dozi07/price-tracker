from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from db.engine import Base


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


class ProductPriceHistory(Base):
    __tablename__ = "product_price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    product = relationship("Product", back_populates="price_history")