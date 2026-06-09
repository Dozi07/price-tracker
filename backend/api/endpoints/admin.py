from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from api.dependencies import get_db

router = APIRouter(tags=["System / Admin"])


@router.post("/system/update-prices")
def trigger_price_update(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Локальный импорт разрывает цикл! Python вызовет его только при клике на кнопку,
    # когда всё приложение уже полностью загрузится в память.
    from services.price_monitor import update_all_product_prices

    background_tasks.add_task(update_all_product_prices, db)
    return {"message": "Процесс фонового обновления цен успешно запущен."}