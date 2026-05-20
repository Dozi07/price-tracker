from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.Creating_eng_db import Base

class ProductPriceHistory(Base):
    __tablename__ = "product_price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    product = relationship("Product", back_populates="price_history")