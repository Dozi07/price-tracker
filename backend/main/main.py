from models.Users import User 
from models.Product import Product
from models.Category import Category
from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from main.registrated import router as auth_router
from main.login import router as login_router
from main.product_create import router as product_create_router
from main.create_db import create
from main.get_product import router as product_get_router
from main.categories import router as categories_router

create()
app = FastAPI()


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(login_router)
app.include_router(product_create_router)
app.include_router(product_get_router)
app.include_router(categories_router)