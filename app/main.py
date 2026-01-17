from scraper import PriceScraper
from providers import CryptoProvider
from database import init_db, Session, Product, PriceHistory
import time


def track():
    init_db()
    session = Session()
    # Scraper zostawiamy dla produktów z Empiku, CryptoProvider dla walut
    scraper = PriceScraper()
    api = CryptoProvider()

    # Dodajemy Bitcoin do bazy jeśli go nie ma
    if not session.query(Product).filter_by(url="api://bitcoin").first():
        btc = Product(name="Bitcoin", url="api://bitcoin")
        session.add(btc)
        session.commit()

    print("--- START MONITORA (Ctrl+C aby zatrzymać) ---")
    try:
        while True:
            # 1. Pobieranie ceny z API (Bitcoin)
            btc_product = session.query(Product).filter_by(url="api://bitcoin").one()
            price = api.get_price("bitcoin")

            if price:
                entry = PriceHistory(price=price, product=btc_product)
                session.add(entry)
                session.commit()
                print(f"[{time.strftime('%H:%M:%S')}] Bitcoin: {price} PLN")

            # [Opcjonalnie] Tutaj możesz dodać sprawdzanie Empiku raz na godzinę

            time.sleep(30)  # Czekaj 30 sekund przed kolejnym sprawdzeniem
    except KeyboardInterrupt:
        print("\nZatrzymano monitor.")
    finally:
        session.close()


if __name__ == "__main__":
    track()