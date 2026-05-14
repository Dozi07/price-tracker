from models.Users import User
from models.Product import Product

from database.Creating_eng_db import Base, engine


def create():
    return Base.metadata.create_all(engine)



