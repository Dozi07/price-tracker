from database.Creating_eng_db import Base, engine

from models.Users import User
from models.Product import Product
from models.Category import Category

def create():
    return Base.metadata.create_all(engine)



