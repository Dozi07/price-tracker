from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Импортируем "каталог" из моего файла

class User(Base): # таблица user
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    