from scraper import PriceScraper
from database import init_db, Session, Product, PriceHistory

def track_prices():
    # 1. Przygotuj bazę danych
    init_db()
    session = Session()
    scraper = PriceScraper()

    # 2. Zdefiniuj produkty (w przyszłości możesz je dodawać z konsoli)
    tracked_items = [
        {"name": "Schronisko - S. Gortych", "url": "https://www.empik.com/schronisko-ktore-zostalo-zapomniane-slawek-gortych,p1607769909,ksiazka-p"}
    ]

    for item in tracked_items:
        # Sprawdź czy produkt jest już w bazie
        product = session.query(Product).filter_by(url=item['url']).first()
        if not product:
            product = Product(name=item['name'], url=item['url'])
            session.add(product)
            session.commit()

        print(f"Pobieram cenę dla: {product.name}...")
        current_price = scraper.get_universal_price(product.url)

        if current_price:
            # 3. Zapisz nową cenę do historii
            new_price_entry = PriceHistory(price=current_price, product=product)
            session.add(new_price_entry)
            session.commit()
            print(f"Zapisano cenę: {current_price} PLN")
        else:
            print("Nie udało się pobrać ceny.")

    session.close()

if __name__ == "__main__":
    track_prices()