from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database.Creating_eng_db import Base  # Импортируем "каталог" из моего файла

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    url = Column(String, nullable = False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)