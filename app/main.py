from scraper import PriceScraper
from providers import CryptoProvider
from database import init_db, Session, Product, PriceHistory
import time


def track():

    curr = "solana"

    init_db()
    session = Session()
    scraper = PriceScraper()
    api = CryptoProvider()

    # Dodajemy walutę do bazy jeśli jej nie ma
    if not session.query(Product).filter_by(url=f"api://{curr}").first():
        p = Product(name=curr.capitalize(), url=f"api://{curr}")
        session.add(p)
        session.commit()

    print("--- START MONITORA (Ctrl+C aby zatrzymać) ---")
    try:
        while True:
            # Pobieranie ceny z API
            product = session.query(Product).filter_by(url=f"api://{curr}").one()
            price = api.get_price(curr)

            if price:
                entry = PriceHistory(price=price, product=product)
                session.add(entry)
                session.commit()
                print(f"[{time.strftime('%H:%M:%S')}] {curr.capitalize()}: {price} PLN")

            time.sleep(30)
    except KeyboardInterrupt:
        print("\nZatrzymano monitor.")
    finally:
        session.close()


if __name__ == "__main__":
    track()