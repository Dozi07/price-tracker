from sqlalchemy import Column, Integer, String
from db.engine import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=1)
    email = Column(String, unique=1, nullable=0)
    hashed_password = Column(String, unique=0, nullable=0)

