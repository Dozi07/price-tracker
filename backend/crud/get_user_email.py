from sqlalchemy.orm import Session
from models.Users import User

def get_user_email(db : Session, email:str):
    return db.query(User).filter(User.email == email).first()
