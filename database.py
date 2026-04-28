from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:1111@localhost:5432/price_tracker" #указываем адрес бд

engine = create_engine(DATABASE_URL) #создаем движок с помощью которого необходимые объекты будут получать доступ к бд

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # создаем объект который будет открывать нашу базу данных

Base = declarative_base() # класс от которого наследуются другие таблицы и будут хранится в нем
