from http.client import HTTPException
from crud.CreateNewUser import CreateNewUser
from fastapi import FastAPI, Depends, APIRouter
from crud.get_user_email import get_user_email
from schemas.User_for_front import User_for_front
from schemas.UserCreate import UserCreate
from main.get_db import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Registration"])

@router.post("/registrated", response_model=User_for_front)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if(get_user_email(db, email=user.email)):
        raise HTTPException(status_code=400, detail="User is already registered")
    return CreateNewUser(db, user)
