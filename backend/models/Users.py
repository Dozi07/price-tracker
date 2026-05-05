from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.Creating_eng_db import Base  # Импортируем "каталог" из моего файла


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=1, unique=1, index=1, nullable=1)
    email = Column(String, unique=1, nullable=0)
    hashed_password = Column(String, unique=0, nullable=0)

