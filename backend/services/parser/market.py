import os
import re
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_yandex_market_product(url: str) -> dict:
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")

    # Отключаем картинки для скорости загрузки самой страницы
    # (Сама ссылка на картинку в коде страницы при этом останется)
    options.add_argument("--blink-settings=imagesEnabled=false")

    profile_path = os.path.join(os.getcwd(), "yandex_market_profile")
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = None
    try:
        driver = uc.Chrome(options=options, version_main=147)
        driver.get(url)

        print("Загрузка страницы... Ожидаем полную прогрузку скриптов Яндекса...")
        time.sleep(7)  # Увеличили паузу, чтобы скрипты динамической цены успели отработать

        # Проверка на капчу
        current_url = driver.current_url.lower()
        if any(sig in current_url for sig in
               ["captcha", "showcaptcha", "validate"]) or "Введите код" in driver.page_source:
            print("\n🛑 Пожалуйста, решите капчу в окне браузера!")
            input("После появления карточки товара НАЖМИТЕ ENTER ТУТ...")
            time.sleep(2)

        # 1. ПАРСИНГ НАЗВАНИЯ
        name = "Без названия"
        try:
            wait = WebDriverWait(driver, 10)
            name_el = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            name = name_el.text.strip()
        except Exception:
            try:
                name_el = driver.find_element(By.CSS_SELECTOR, "[data-auto='productCardTitle']")
                name = name_el.text.strip()
            except Exception:
                pass

        # 2. ПАРСИНГ ЦЕНЫ
        price = 0

        # --- МЕТОД 1: Ищем мета-теги SEO ---
        try:
            meta_price = driver.find_element(By.XPATH, "//meta[@property='og:price:amount' or @itemprop='price']")
            price_content = meta_price.get_attribute("content")
            if price_content:
                clean_meta_price = re.sub(r'\D', '', price_content)
                if clean_meta_price:
                    price = int(clean_meta_price)
                    print(f"✓ Цена успешно извлечена из мета-тегов карточки: {price} ₽")

            if price == 0:
                meta_price_alt = driver.find_element(By.XPATH,
                                                     "//meta[contains(@name, 'price') or contains(@property, 'price')]")
                price_content_alt = meta_price_alt.get_attribute("content")
                if price_content_alt:
                    clean_alt = re.sub(r'\D', '', price_content_alt)
                    if clean_alt:
                        price = int(clean_alt)
        except Exception:
            pass

        # --- МЕТОД 2: По атрибутам элементов ---
        if price == 0:
            attribute_selectors = [
                "[data-auto='price-value']",
                "[data-auto='mainPrice']",
                "[class*='PriceValue']",
                "span[data-tid]"
            ]

            for selector in attribute_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for el in elements:
                        for attr in ["value", "data-value", "data-price", "content"]:
                            val = el.get_attribute(attr)
                            if val and any(char.isdigit() for char in val):
                                clean_val = re.sub(r'\D', '', val)
                                if clean_val:
                                    price = int(clean_val)
                                    break
                        if price > 0:
                            break
                    if price > 0:
                        print(f"✓ Цена успешно извлечена через внутренний атрибут: {price} ₽")
                        break
                except:
                    continue

        # --- МЕТОД 3: Regex по JSON-данным ---
        if price == 0:
            print("⚠️ Стандартные методы не дали результат. Запуск глубокого сканирования кода страницы...")
            html_source = driver.page_source

            price_matches = re.findall(r'"price"\s*:\s*\{\s*"value"\s*:\s*(\d+)', html_source)
            if not price_matches:
                price_matches = re.findall(r'"currentPrice"\s*:\s*\{\s*"value"\s*:\s*(\d+)', html_source)

            if price_matches:
                for potential_price in price_matches:
                    p_int = int(potential_price)
                    if p_int > 100:
                        price = p_int
                        print(f"✓ Цена успешно извлечена из скрытого JSON страницы: {price} ₽")
                        break

        if price == 0:
            print("❌ Не удалось извлечь цену ни одним из способов. Возможно, товара нет в наличии.")

        # 3. ПАРСИНГ КАРТИНКИ
        image_url = ""
        try:
            # Метод 1: Ищем в мета-тегах (работает как на Ozon)
            meta_img = driver.find_element(By.XPATH, "//meta[@property='og:image']")
            img_content = meta_img.get_attribute("content")
            if img_content:
                image_url = img_content
                print("✓ Картинка успешно извлечена из og:image")
        except Exception:
            try:
                # Метод 2: Ищем через микроразметку товара
                img_el = driver.find_element(By.XPATH, "//*[@itemprop='image']")
                img_src = img_el.get_attribute("src")
                if not img_src:
                    img_src = img_el.get_attribute("content")
                if img_src:
                    image_url = img_src
                    print("✓ Картинка успешно извлечена из микроразметки")
            except Exception:
                print("❌ Не удалось найти картинку товара.")

        # ВОЗВРАЩАЕМ ЕДИНЫЙ СЛОВАРЬ (как в Ozon)
        return {
            "name": name,
            "price": price,
            "image_url": image_url
        }

    except Exception as e:
        print(f"Ошибка выполнения: {e}")
        return {
            "name": "Ошибка парсинга ЯМ",
            "price": 0,
            "image_url": ""
        }
    finally:
        if driver:
            driver.quit()