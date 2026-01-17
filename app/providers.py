import requests
from typing import Optional

class CryptoProvider:
    @staticmethod
    def get_price(coin_id: str = "bitcoin") -> Optional[float]:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=pln"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return float(data[coin_id]['pln'])
        except Exception as e:
            print(f"Błąd API ({coin_id}): {e}")
            return None