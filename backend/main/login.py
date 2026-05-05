from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from crud.get_user_email import get_user_email
from schemas.User_for_front import User_for_front
from schemas.UserCreate import UserCreate
from main.get_db import get_db
from Security.verify_pas import verify_pas

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=User_for_front)
def login (user: UserCreate, db: Session = Depends(get_db)):
    if get_user_email(db, email=user.email) == 0:
        raise HTTPException(status_code=404, detail="User does not exist")
    if verify_pas(user.password, get_user_email(db, email=user.email).hashed_password):
        return get_user_email(db, email=user.email)
    else:raise HTTPException(status_code=401, detail="Incorrect password")