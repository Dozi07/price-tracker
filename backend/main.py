from datetime import date
from db.engine import SessionLocale
from product import Product, ProductPriceHistory


def update_product_price(product_id: int, parser_func):
    """
    Обновляет товар:
    - запускает парсер по URL товара
    - получает новую цену и название
    - обновляет product
    - записывает цену в product_price_history

    :param product_id: ID товара в таблице product
    :param parser_func: функция парсера, которая принимает url и возвращает dict:
                        {
                            "name": str,
                            "price": int
                        }
    """
    session = SessionLocale()

    try:
        # 1. Получаем товар из БД
        product = session.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise ValueError(f"Товар с id={product_id} не найден")

        # 2. Перезапускаем парсер
        parsed_data = parser_func(product.url)

        if not parsed_data:
            raise ValueError("Парсер не вернул данные")

        new_name = parsed_data.get("name")
        new_price = parsed_data.get("price")

        if new_name is None or new_price is None:
            raise ValueError("Парсер должен вернуть name и price")

        # 3. Обновляем карточку товара
        product.name = new_name
        product.price = int(new_price)

        # 4. Добавляем запись в историю цены
        price_history = ProductPriceHistory(
            product_id=product.id,
            price=int(new_price),
            date=date.today()
        )

        session.add(price_history)
        session.commit()

        return {
            "status": "success",
            "product_id": product.id,
            "name": product.name,
            "price": product.price
        }

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()
