from db.engine import Base, engine
from models import category, notification, product, users

def create():
    return Base.metadata.create_all(engine)



