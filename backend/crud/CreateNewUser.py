from sqlalchemy.orm import Session
from models.Users import User
from schemas.UserCreate import UserCreate
from Security.hash_pas import hash_pas

def CreateNewUser(db : Session, user : UserCreate):
    new_user = User(email = user.email, hashed_password = hash_pas(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

