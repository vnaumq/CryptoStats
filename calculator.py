import json
from datetime import datetime
from api_client import CryptoAPI

class PortfolioCalculator:
    def __init__(self, portfolio_file):
        self.portfolio_file = portfolio_file
        self.api = CryptoAPI()
        self.load_portfolio()

    def load_portfolio(self):
        """Загрузка портфеля из файла"""
        try:
            with open(self.portfolio_file, 'r') as f:
                self.portfolio = json.load(f)
        except FileNotFoundError:
            print(f"Файл {self.portfolio_file} не найден. Создан шаблон.")
            self.portfolio = {
                "assets": [],
                "fiat_currency": "USDT"
            }
            self.save_portfolio()

    def save_portfolio(self):
        """Сохранение портфеля в файл"""
        with open(self.portfolio_file, 'w') as f:
            json.dump(self.portfolio, f, indent=2)

    def calculate_total_balance(self):
        """Расчет общего баланса"""
        total = 0
        asset_details = []

        for asset in self.portfolio['assets']:
            symbol = asset['symbol']
            amount = asset['amount']
            fiat = self.portfolio.get('fiat_currency', 'USDT')

            # Для стейблкоинов
            if asset.get('is_stablecoin', False) and symbol.upper() == fiat.upper():
                price = 1.0
            else:
                price = self.api.get_price(symbol, fiat)

            value = amount * price
            total += value

            asset_details.append({
                'symbol': symbol,
                'amount': amount,
                'price': price,
                'value': value,
                'percentage': 0  # будет рассчитано позже
            })

        # Расчет процентов
        for asset in asset_details:
            if total > 0:
                asset['percentage'] = (asset['value'] / total) * 100

        return {
            'total': total,
            'assets': asset_details,
            'currency': self.portfolio.get('fiat_currency', 'USDT'),
            'timestamp': datetime.now().isoformat()
        }

    def add_asset(self, symbol, amount, name=None, is_stablecoin=False):
        """Добавление актива в портфель"""
        # Проверяем, есть ли уже такой актив
        for asset in self.portfolio['assets']:
            if asset['symbol'].upper() == symbol.upper():
                asset['amount'] += amount
                break
        else:
            self.portfolio['assets'].append({
                'symbol': symbol.upper(),
                'amount': amount,
                'name': name or symbol,
                'is_stablecoin': is_stablecoin
            })

        self.save_portfolio()