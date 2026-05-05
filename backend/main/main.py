from fastapi import FastAPI, Depends, APIRouter
from main.registrated import router as auth_router
from main.login import router as login_router
from main.create_db import create

create()
app = FastAPI()

app.include_router(auth_router)
app.include_router(login_router)