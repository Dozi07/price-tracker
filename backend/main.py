import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints.auth import router as auth_router
from api.endpoints.product import router as products_router
from api.endpoints.categories import router as categories_router
from api.endpoints.notifications import router as notifications_router
from api.endpoints.admin import router as admin_router
from db.init_db import create


from db.engine import SessionLocale  # Проверь этот импорт, откуда у тебя берется сессия базы
from services.price_monitor import update_all_product_prices  # Замени update_prices на реальное имя твоей функции парсинга



async def price_updater_task():

    while True:
        print("[BACKGROUND] Запуск автоматического обновления цен...")
        db = SessionLocale()
        try:

            update_all_product_prices(db)
            print("[BACKGROUND] Автоматическое обновление цен успешно завершено.")
        except Exception as e:
            print(f"[BACKGROUND ERROR] Ошибка при обновлении цен: {e}")
        finally:
            db.close()


        await asyncio.sleep(1800)



@asynccontextmanager
async def lifespan(app: FastAPI):

    updater_task = asyncio.create_task(price_updater_task())
    yield

    updater_task.cancel()


create()


app = FastAPI(
    title="Price Tracker API",
    version="1.0.0",
    lifespan=lifespan
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

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(notifications_router)
app.include_router(admin_router)