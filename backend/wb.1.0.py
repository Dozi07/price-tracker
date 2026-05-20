import undetected_chromedriver as uc
import time
import re
import os
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_wb_product(url: str) -> dict:
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")

    # Путь к профилю
    profile_path = os.path.join(os.getcwd(), "wb_user_profile")
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = None
    try:
        driver = uc.Chrome(options=options, version_main=147)
        driver.get(url)

        # 1. Даем странице время на базовую загрузку
        time.sleep(3)

        # 2. ПРОКРУТКА (Критически важно для WB)
        # Прокручиваем немного вниз, чтобы сработали скрипты подгрузки цен
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

        wait = WebDriverWait(driver, 10)

        # 3. ИЗВЛЕКАЕМ НАЗВАНИЕ (пробуем несколько селекторов)
        name = "Не найдено"
        name_selectors = ['h1.product-page__title', 'h1', '.product-page__header h1']
        for selector in name_selectors:
            try:
                el = driver.find_element(By.CSS_SELECTOR, selector)
                if el.text.strip():
                    name = el.text.strip()
                    break
            except:
                continue

        # 4. ИЗВЛЕКАЕМ ЦЕНУ (пробуем самые частые варианты WB)
        price = 0
        # Список селекторов для цены (WB часто их меняет)
        price_selectors = [
            ".price-block__final-price",
            "ins.price-block__final-price",
            ".product-page__price-block ins",
            "span.price-block__wallet-price",  # Цена с кошельком
            ".n-price"
        ]

        found_price_text = ""
        for selector in price_selectors:
            try:
                # Ждем появления хотя бы одного из селекторов
                el = driver.find_element(By.CSS_SELECTOR, selector)
                if el.text.strip():
                    found_price_text = el.text.strip()
                    break
            except:
                continue

        # Если через классы не нашли, ищем по тегу 'ins' (обычно цена там)
        if not found_price_text:
            try:
                el = driver.find_element(By.TAG_NAME, "ins")
                found_price_text = el.text
            except:
                pass

        # Очистка цены
        if found_price_text:
            clean_price = re.sub(r'\D', '', found_price_text)
            if clean_price:
                price = int(clean_price)

        return {
            "name": name,
            "price": price
        }

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {"name": "Ошибка", "price": 0}
    finally:
        if driver:
            driver.quit()


#if __name__ == "__main__":
    # Тестовая ссылка
    #url = "https://www.wildberries.ru/catalog/235691524/detail.aspx?targetUrl=MI"
    #data = parse_wb_product(url)

    #print("\n" + "=" * 30)
    #print(f"Товар: {data['name']}")
    #print(f"Цена: {data['price']} ₽")
    #print("=" * 30)

#https://www.wildberries.ru/catalog/235691524/detail.aspx?targetUrl=MI
