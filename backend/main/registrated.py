from http.client import HTTPException
from crud.CreateNewUser import CreateNewUser
from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from crud.get_user_email import get_user_email
from schemas.User_for_front import User_for_front
from schemas.UserCreate import UserCreate
from main.get_db import get_db

router = APIRouter(tags=["Registration"])

@router.post("/registrated", response_model=User_for_front)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if(get_user_email(db, email=user.email)):
       raise HTTPException(stasus_code = 400, detail = "User is alredy registreated")
    return CreateNewUser(db, user)
