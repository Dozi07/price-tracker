import pandas as pd
import undetected_chromedriver as uc
import time
import re
import os
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_wb_data(urls):
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    profile_path = os.path.join(os.getcwd(), "wb_profile")
    options.add_argument(f"--user-data-dir={profile_path}")

    print("🚀 Запуск браузера...")
    driver = uc.Chrome(options=options, version_main=147)

    results = []

    try:
        for url in urls:
            try:
                print(f"\n--- 🔎 Загрузка: {url} ---")
                driver.get(url)

                time.sleep(random.uniform(5, 7))

                driver.execute_script("window.scrollBy(0, 400)")
                time.sleep(1)

                try:
                    name_element = driver.find_element(By.TAG_NAME, "h1")
                    name = name_element.text.strip()
                except:
                    name = "Название не найдено"

                price_wallet = "0"
                price_base = "0"

                price_selectors = [
                    "ins.price-block__final-price",  
                    ".price-block__wallet-price",  
                    ".price-block__content", 
                    ".product-page__price-block"  
                ]

                found_prices = []
                for selector in price_selectors:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for el in elements:
                        text = el.text.replace('\xa0', '').replace(' ', '').replace('₽', '')
                        nums = re.findall(r'\d+', text)
                        found_prices.extend([int(n) for n in nums if int(n) > 50])

                if found_prices:
                    unique_prices = sorted(list(set(found_prices)))
                    price_wallet = unique_prices[0]
                    price_base = unique_prices[1] if len(unique_prices) > 1 else unique_prices[0]
                else:
                    try:
                        all_page_text = driver.find_element(By.TAG_NAME, "body").text
                        raw_prices = re.findall(r'(\d[\d\s]*)\s?₽', all_page_text)
                        clean_prices = sorted([int(p.replace(' ', '').replace('\xa0', '')) for p in raw_prices if int(p.replace(' ', '')) > 50])
                        if clean_prices:
                            price_wallet = clean_prices[0]
                            price_base = clean_prices[1] if len(clean_prices) > 1 else clean_prices[0]
                    except:
                        pass

                try:
                    seller_el = driver.find_element(By.CLASS_NAME, "seller-info__name")
                    seller = seller_el.text.strip()
                except:
                    seller = "Wildberries"

                item = {
                    'Цена с Кошельком': f"{price_wallet} ₽",
                    'Обычная цена': f"{price_base} ₽",
                }
                results.append(item)
                return item

            except Exception as e:
                print(f"⚠️ Ошибка на ссылке: {e}")

    finally:
        driver.quit()

    if results:
        df = pd.DataFrame(results)
        df.to_excel('wb_data.xlsx', index=False)
        print("\n📁 Результаты сохранены в wb_data.xlsx")

#if __name__ == "__main__":
    #test_urls = [
        #"https://www.wildberries.ru/catalog/225719505/detail.aspx?targetUrl=MI",
      #  "https://www.wildberries.ru/catalog/817440992/detail.aspx?targetUrl=MI"
  #  ]
  #  get_wb_data(test_urls)
