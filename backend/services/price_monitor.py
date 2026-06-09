from datetime import date
from sqlalchemy.orm import Session
from models.product import Product, ProductPriceHistory
from crud.notification import create_notification
from services.parser.ozon import parse_ozon_product
from services.parser.market import parse_yandex_market_product


def get_marketplace_id_from_url(url: str) -> int:
    """
    Автоматически определяет маркетплейс по подстроке в URL.
    1 - Ozon, 2 - Wildberries, 3 - Yandex Market, 0 - Неизвестно
    """
    url_lower = url.lower()
    if "ozon.ru" in url_lower:
        return 1
    elif "wildberries.ru" in url_lower or "wb.ru" in url_lower:
        return 2
    elif "market.yandex.ru" in url_lower:
        return 3
    return 0


def update_all_product_prices(db: Session):
    """
    Пробегается по всем товарам в БД, автоматически определяет маркетплейс по URL,
    парсит актуальные цены, обновляет их в базе, записывает в историю
    и создает уведомления при снижении цены.
    """
    print("🚀 Запуск фонового обновления цен...")
    products = db.query(Product).all()

    if not products:
        print("ℹ️ В базе данных пока нет товаров для обновления.")
        return

    for product in products:
        # Автоматически определяем маркетплейс по URL товара
        marketplace_id = get_marketplace_id_from_url(product.url)

        marketplace_names = {1: "Ozon", 2: "Wildberries", 3: "Yandex Market", 0: "Неизвестно"}
        print(
            f"🔄 Проверяем товар: '{product.name}' (ID: {product.id}, Маркетплейс: {marketplace_names[marketplace_id]})")

        parsed_data = None

        try:
            # 1. Вызываем нужный парсер на основе определенного ID
            if marketplace_id == 1:
                parsed_data = parse_ozon_product(product.url)
            elif marketplace_id == 3:
                parsed_data = parse_yandex_market_product(product.url)
            elif marketplace_id == 2:
                print(f"⚠️ Парсер Wildberries для товара ID {product.id} временно недоступен (ждёт обновления wb.py).")
                continue
            else:
                print(f"❌ Не удалось определить маркетплейс для ссылки: {product.url}")
                continue

            # Проверяем, что парсер вернул корректные данные
            if not parsed_data or parsed_data.get("price", 0) == 0:
                print(f"❌ Не удалось спарсить актуальную цену для товара ID {product.id}")
                continue

            new_price = int(parsed_data["price"])
            old_price = product.price

            # 2. Если цена изменилась, обновляем её в базе данных
            if new_price != old_price:
                product.price = new_price

                # 3. Добавляем новую точку на график (ProductPriceHistory)
                new_history = ProductPriceHistory(
                    product_id=product.id,
                    price=new_price,
                    date=date.today()
                )
                db.add(new_history)

                # 4. СИСТЕМА УВЕДОМЛЕНИЙ: Если цена СНИЗИЛАСЬ, генерируем уведомление в БД
                if new_price < old_price:
                    discount = old_price - new_price
                    category_name = product.category.name if product.category else "Общая"

                    notification_text = f"Цена снизилась на {discount} ₽!"

                    create_notification(
                        db=db,
                        product_name=product.name,
                        category_name=category_name,
                        text=notification_text,
                        user_id=product.user_id  # Уведомление привязывается к владельцу товара
                    )
                    print(f"🔔 Создано уведомление для пользователя {product.user_id}: цена упала на {discount}₽")

                db.commit()
                print(f"✅ Цена успешно обновлена: {old_price} ₽ -> {new_price} ₽")
            else:
                print(f"⚖️ Цена не изменилась ({old_price} ₽).")

        except Exception as e:
            print(f"💥 Критическая ошибка при обновлении товара ID {product.id}: {e}")
            db.rollback()  # Откатываем транзакцию в случае падения, чтобы не вешать БД

    print("🏁 Процесс фонового обновления всех цен завершен.")