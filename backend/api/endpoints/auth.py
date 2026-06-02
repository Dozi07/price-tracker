from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.dependencies import get_db
from schemas.user import UserCreate, User_for_front, Token
from crud.user import get_user_email, CreateNewUser
from core.security import verify_pas, create_access_token

router = APIRouter(
    tags=["Authentication & Registration"]
)

@router.post("/registrated", response_model=User_for_front)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="User is already registered")
    return CreateNewUser(db, user)


@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_email(db, email=user.email)

    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if verify_pas(user.password, db_user.hashed_password):
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")