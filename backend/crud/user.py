from sqlalchemy.orm import Session
from models.users import User
from schemas.user import UserCreate

from core.security import hash_pas

def CreateNewUser(db : Session, user : UserCreate):
    new_user = User(email = user.email, hashed_password = hash_pas(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_email(db : Session, email:str):
    return db.query(User).filter(User.email == email).first()
