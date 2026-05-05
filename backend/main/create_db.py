from database.Creating_eng_db import Base, engine
from models.Users import User


def create():
    return Base.metadata.create_all(engine)



