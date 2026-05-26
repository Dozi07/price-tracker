import undetected_chromedriver as uc
import time
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_wb_product(url: str) -> dict:
    """Бронебойный парсер Wildberries с явными ожиданиями"""
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")

    profile_path = os.path.join(os.getcwd(), "wb_user_profile")
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = None
    try:
        # Убедись, что тут стоит твоя версия Chrome (148 или 149)
        driver = uc.Chrome(options=options, version_main=148)
        driver.get(url)

        print("🌐 Открыли страницу WB, ждем подгрузки скриптов...")

        # ЭКСТРЕМАЛЬНО ВАЖНО: Ждем до 15 секунд, пока не появится хотя бы один тег h1
        try:
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            print("✓ Структура страницы загружена.")
        except Exception:
            print("⚠️ Заголовок не появился за 15 сек. Возможно вылезла капча WB.")

        # Делаем прокрутку, чтобы спровоцировать подгрузку фото
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(2)

        # 1. ИЗВЛЕКАЕМ НАЗВАНИЕ
        name = "Без названия"
        try:
            # Ищем все заголовки и берем первый нормальный
            h1_elements = driver.find_elements(By.TAG_NAME, "h1")
            for el in h1_elements:
                text = el.text.strip()
                if text and len(text) > 5:  # Игнорируем рейтинги типа "4,9"
                    name = text
                    print(f"✓ Название найдено: {name}")
                    break
        except Exception:
            pass

        # 2. ИЗВЛЕКАЕМ ЦЕНУ
        price = 0
        price_selectors = [
            ".price-block__final-price",
            "ins.price-block__final-price",
            "span.price-block__wallet-price",
            ".n-price"
        ]

        found_price_text = ""
        for selector in price_selectors:
            try:
                el = driver.find_element(By.CSS_SELECTOR, selector)
                if el.text.strip():
                    found_price_text = el.text.strip()
                    break
            except Exception:
                continue

        if not found_price_text:
            try:
                el = driver.find_element(By.TAG_NAME, "ins")
                found_price_text = el.text
            except Exception:
                pass

        if found_price_text:
            clean_price = re.sub(r'\D', '', found_price_text)
            if clean_price:
                price = int(clean_price)
                print(f"✓ Цена найдена: {price} ₽")

        # 3. ИЗВЛЕКАЕМ КАРТИНКУ
        image_url = ""
        img_selectors = [
            ".photo-zoom__preview img",
            ".zoom-image-container img",
            ".product-page__slider-wrap img",
            ".slide__content img",
            "img.j-zoom-image"
        ]

        for selector in img_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    src = el.get_attribute("src")
                    # ЖЕСТКИЙ ФИЛЬТР: Берем только реальные фото (basket), а не логотипы (og_img)
                    if src and "basket" in src and "og_img" not in src.lower():
                        image_url = src
                        print("✓ Картинка успешно найдена в галерее")
                        break
                if image_url:
                    break
            except Exception:
                continue

        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

        return {
            "name": name,
            "price": price,
            "image_url": image_url
        }

    except Exception as e:
        print(f"❌ Критическая ошибка парсинга WB: {e}")
        return {
            "name": "Ошибка парсинга WB",
            "price": 0,
            "image_url": ""
        }
    finally:
        if driver:
            driver.quit()