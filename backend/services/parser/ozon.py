import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import re
import os
import random


def parse_ozon_product(url: str) -> dict:
    """Очищенный парсер Ozon для интеграции в бэкенд"""
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")

    profile_path = os.path.join(os.getcwd(), "ozon_user_profile")
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = None

    try:
        driver = uc.Chrome(options=options, version_main=147)
        driver.get(url)

        time.sleep(random.uniform(5, 8))
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        name_el = soup.find("h1")
        name = name_el.text.strip() if name_el else "Без названия"

        price = 0
        price_widget = soup.find("div", {"data-widget": "webPrice"})

        if price_widget:
            raw_text = (
                price_widget
                .get_text("|", strip=True)
                .replace("\u2009", "")
                .replace(" ", "")
            )

            clean_numbers = re.findall(r"\d+", raw_text)
            valid_prices = [int(n) for n in clean_numbers if len(n) >= 3]

            if valid_prices:
                unique_prices = sorted(list(set(valid_prices)))
                price = unique_prices[0]

        image = ""

        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            image = og_image["content"]

        return {
            "name": name,
            "price": price,
            "image_url": image
        }

    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return {
            "name": "Ошибка парсинга Ozon",
            "price": 0,
            "image_url": ""
        }

    finally:
        if driver:
            driver.quit()