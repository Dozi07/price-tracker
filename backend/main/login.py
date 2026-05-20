from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from crud.get_user_email import get_user_email
from schemas.JWTKey import Token
from schemas.UserCreate import UserCreate
from main.get_db import get_db
from Security.verify_pas import verify_pas
from Security.JWT_create import create_access_token
router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login (user: UserCreate, db: Session = Depends(get_db)):
    if not get_user_email(db, email=user.email):
        raise HTTPException(status_code=404, detail="User does not exist")
    if verify_pas(user.password, get_user_email(db, email=user.email).hashed_password):
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    else:raise HTTPException(status_code=401, detail="Incorrect password")

