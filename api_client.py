import requests
from config import BINANCE_API_URL

class CryptoAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_price_from_binance(self, symbol, fiat="USDT"):
        """Получение цены с Binance"""
        try:
            pair = f"{symbol}{fiat}"
            response = self.session.get(
                f"{BINANCE_API_URL}?symbol={pair}",
                timeout=10
            )
            data = response.json()
            return float(data['price'])
        except Exception as e:
            print(f"Ошибка получения цены {symbol} с Binance: {e}")
            return None

    def get_price(self, symbol, fiat="USDT"):
        """Основной метод получения цены"""

        price = self.get_price_from_binance(symbol, fiat)
        if price:
            return price

        print(f"Не удалось получить цену для {symbol}")
        return 0.0