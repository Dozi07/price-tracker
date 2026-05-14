from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.Creating_eng_db import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    #к какой категории принадлежит товар
    category_id = Column(Integer, ForeignKey("category.id"))

    #связь с таблицей категорий
    category = relationship("Category", back_populates="products")