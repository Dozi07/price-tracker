from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:123456@localhost:5432/mydb"

engine = create_engine(DATABASE_URL)

SessionLocale = sessionmaker(autocommit = 0, autoflush = 0, bind = engine)

Base = declarative_base()