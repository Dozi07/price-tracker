from sqlalchemy.orm import Session
import models, schematic
import bcrypt



def hash_password(password: str) -> str:

    pwd_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(pwd_bytes, salt)

    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def get_user(db: Session, user_id : int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db : Session, email : str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user : schematic.UserCreate):
    new_user = models.User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user