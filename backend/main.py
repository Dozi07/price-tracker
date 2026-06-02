from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints.auth import router as auth_router
from api.endpoints.product import router as products_router
from api.endpoints.categories import router as categories_router
from db.init_db import create

create()

app = FastAPI(
    title="Price Tracker API",
    version="1.0.0"
)

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

app.include_router(auth_router)       # Здесь теперь и регистрация, и логин
app.include_router(products_router)   # Здесь добавление, удаление и получение товаров
app.include_router(categories_router) # Здесь управление категориями