from db.engine import Base, engine


def create():
    return Base.metadata.create_all(engine)



