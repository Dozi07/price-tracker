from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.Creating_eng_db import Base 


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=1)
    email = Column(String, unique=1, nullable=0)
    hashed_password = Column(String, unique=0, nullable=0)

