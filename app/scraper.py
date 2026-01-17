from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from typing import Optional
import time


class PriceScraper:
    def __init__(self):
        # [PRO TIP] Safari ma mniej opcji konfiguracyjnych niż Chrome,
        # ale jest natywne dla Twojego macOS.
        self.options = Options()
        # Safari nie wspiera typowego trybu 'headless' tak łatwo jak Chrome,
        # więc na sekundę zobaczysz okno przeglądarki – to normalne przy testach.
        self.driver = webdriver.Safari(options=self.options)

    def get_empik_price(self, url: str) -> Optional[float]:
        try:
            self.driver.get(url)
            # [PRO TIP] Czekamy, aż strona "osiądzie"
            time.sleep(4)

            # Próbujemy znaleźć cenę w metatagach (najpewniejsze w Empiku)
            element = self.driver.find_element(By.CSS_SELECTOR, 'meta[property="product:price:amount"]')
            price_str = element.get_attribute("content")

            if price_str:
                # Zamieniamy ewentualny przecinek na kropkę i rzutujemy na float
                return float(price_str.replace(",", "."))

            return None
        except Exception as e:
            print(f"Błąd Safari: {e}")
            return None
        finally:
            # [WAŻNE] Zamykamy sesję, żeby nie zostawiać otwartych procesów Safari
            self.driver.quit()

    def get_universal_price(self, url: str) -> Optional[float]:
        try:
            self.driver.get(url)
            time.sleep(4)

            # Lista selektorów, które są standardem w e-commerce
            universal_selectors = [
                'meta[property="product:price:amount"]',  # Open Graph
                'meta[itemprop="price"]',  # Schema.org
                'meta[property="og:price:amount"]',  # Inny wariant OG
                'span[itemprop="price"]'  # Tag tekstowy Schema
            ]

            for selector in universal_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    price_val = element.get_attribute("content") or element.text
                    if price_val:
                        # [PRO TIP] Czyścimy tekst ze wszystkiego co nie jest cyfrą lub kropką
                        clean_price = "".join(c for c in price_val if c.isdigit() or c in ".,")
                        return float(clean_price.replace(",", "."))
                except:
                    continue  # Jeśli nie ma tego taga, sprawdź następny

            return None
        except Exception as e:
            print(f"Błąd Safari: {e}")
            return None
        finally:
            # [WAŻNE] Zamykamy sesję, żeby nie zostawiać otwartych procesów Safari
            self.driver.quit()