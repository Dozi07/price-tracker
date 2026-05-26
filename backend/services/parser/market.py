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

    # Отключаем картинки для скорости
    options.add_argument("--blink-settings=imagesEnabled=false")

    profile_path = os.path.join(os.getcwd(), "yandex_market_profile")
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = None
    try:
        driver = uc.Chrome(options=options)
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

        # 1. Парсинг названия
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

        # 2. ПАРСИНГ ЦЕНЫ (Альтернативные методы через атрибуты)
        price = 0

        # --- МЕТОД 1: Ищем мета-теги SEO (Микроразметка Schema.org) ---
        # Яндекс почти всегда встраивает цену в мета-теги для поисковиков Google/Яндекс в чистом виде.
        try:
            meta_price = driver.find_element(By.XPATH, "//meta[@property='og:price:amount' or @itemprop='price']")
            price_content = meta_price.get_attribute("content")
            if price_content:
                clean_meta_price = re.sub(r'\D', '', price_content)
                if clean_meta_price:
                    price = int(clean_meta_price)
                    print(f"✓ Цена успешно извлечена из мета-тегов карточки: {price} ₽")

            # Запасной мета-тег, если первый пустой
            if price == 0:
                meta_price_alt = driver.find_element(By.XPATH,
                                                     "//meta[contains(@name, 'price') or contains(@property, 'price')]")
                price_content_alt = meta_price_alt.get_attribute("content")
                if price_content_alt:
                    clean_alt = re.sub(r'\D', '', price_content_alt)
                    if clean_alt:
                        price = int(clean_alt)
        except Exception:
            pass  # Если мета-тегов нет, идем дальше

        # --- МЕТОД 2: Если мета-теги не сработали, ищем по атрибутам элементов ---
        if price == 0:
            # Селекторы, где цена может лежать внутри атрибутов value, data-value или data-price
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
                        # Проверяем не text, а внутренние свойства тега, куда Яндекс пишет чистые цифры
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

        # --- МЕТОД 3: Экстренный разбор сырого HTML (Regex по JSON-данным страницы) ---
        if price == 0:
            print("⚠️ Стандартные методы не дали результат. Запуск глубокого сканирования кода страницы...")
            html_source = driver.page_source

            # Ищем в коде страницы JSON-структуры Яндекса, где упоминается "price" или "currentPrice"
            # Обычно это блоки типа "currentPrice":{"value":10490} или "price":{"value":10490}
            price_matches = re.findall(r'"price"\s*:\s*\{\s*"value"\s*:\s*(\d+)', html_source)
            if not price_matches:
                price_matches = re.findall(r'"currentPrice"\s*:\s*\{\s*"value"\s*:\s*(\d+)', html_source)

            if price_matches:
                # Берем первое найденное число, исключая слишком маленькие (типа 0 или 1)
                for potential_price in price_matches:
                    p_int = int(potential_price)
                    if p_int > 100:  # Отсекаем ID или флаги
                        price = p_int
                        print(f"✓ Цена успешно извлечена из скрытого JSON страницы: {price} ₽")
                        break

        if price == 0:
            print("❌ Не удалось извлечь цену ни одним из способов. Возможно, товара нет в наличии.")

        return {
            "name": name,
            "price": price
        }

    except Exception as e:
        print(f"Ошибка выполнения: {e}")
        return {"name": "Ошибка", "price": 0}
    finally:
        if driver:
            driver.quit()


#if __name__ == "__main__":
   # url = "https://market.yandex.ru/card/nike-air-monarch-4-cushioning-breathable-lightweight-casual-shoes-mens-gray-41/4739793306?do-waremd5=YtwNiNr1zsGH1rAvMjHOUA&sponsored=1&cpc=sry9wyIdfwDpWJ1VMVnlFU8a1GoU10mi1K73L1xmXroNxvU8MNnJ21j-PKfTJSFamHDS8mYJeSJIMAFsFVP27Q0N8uZr8W3Iwa6pWpnwuuOd6n6P82owSkv3qicOogaWV8qvKCaFmMHlnduUK8OqQ_eriThbZUaQkPue9TBbjp_CDOowAz2ZMh49KcUibtUvFUBxEootGPx4Jbu03gTsXqLJTNG4tQchDlle16T96vAis17YeojC9uso7baYnYw_jK13AqQWsnx7ZbXcAml0RLA_H69FQYsIjOFga9-EWYCV4bnFwg-ds3Zc_tAFkMsM&cc=CjIxNzc5MjY1NzA1Njc2LzczZWU3YzQyOWYyODA5Zjk0OWQ2MTkyMTRjNTIzZmQzLzEvNxCzAYB95u0G&resale_goods=resale_new&ultima=1&show-uid=17792657060081590066206016&showUid=17792657060081590066206016&from-show-uid=17792657060081590066206016"
   # data = parse_yandex_market_product(url)
    #print(f"\n==============================")
    #print(f"Итог парсинга:")
    #print(f"Товар: {data['name']}")
    #print(f"Цена:  {data['price']} ₽")


#https://market.yandex.ru/card/nike-air-monarch-4-cushioning-breathable-lightweight-casual-shoes-mens-gray-41/4739793306?do-waremd5=YtwNiNr1zsGH1rAvMjHOUA&sponsored=1&cpc=sry9wyIdfwDpWJ1VMVnlFU8a1GoU10mi1K73L1xmXroNxvU8MNnJ21j-PKfTJSFamHDS8mYJeSJIMAFsFVP27Q0N8uZr8W3Iwa6pWpnwuuOd6n6P82owSkv3qicOogaWV8qvKCaFmMHlnduUK8OqQ_eriThbZUaQkPue9TBbjp_CDOowAz2ZMh49KcUibtUvFUBxEootGPx4Jbu03gTsXqLJTNG4tQchDlle16T96vAis17YeojC9uso7baYnYw_jK13AqQWsnx7ZbXcAml0RLA_H69FQYsIjOFga9-EWYCV4bnFwg-ds3Zc_tAFkMsM&cc=CjIxNzc5MjY1NzA1Njc2LzczZWU3YzQyOWYyODA5Zjk0OWQ2MTkyMTRjNTIzZmQzLzEvNxCzAYB95u0G&resale_goods=resale_new&ultima=1&show-uid=17792657060081590066206016&showUid=17792657060081590066206016&from-show-uid=17792657060081590066206016