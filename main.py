from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud

import models, schematic, database, crud
from crud import get_user_by_email
from database import *


Base.metadata.create_all(bind=engine) # здесь создаем все таблицы с столбцами, потом убрать create_all

app = FastAPI()

def get_db(): # открывает бд
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=schematic.User)
def create_user(user : schematic.UserCreate, db : Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code = 400, detail="Акаунт с такой почтой уже существует")
    return crud.create_user(db, user)

@app.post("./login", response_model=schematic.UserCreate)
def login(user : schematic.UserCreate, db : Session = Depends(get_db)):
    TempUser = get_user_by_email(db, user.email)
    if not TempUser:
        raise HTTPException(status_code=404, detail="акаунта с такой почтнй не существет")

    if crud.verify_password(user.password, TempUser.password):
        return TempUser
    else: raise HTTPException(status_code= 401, detail="Пароль введен неверно")