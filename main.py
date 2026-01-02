#!/usr/bin/env python3
import schedule
import time
import json
from datetime import datetime
import argparse
from config import PORTFOLIO_FILE, HISTORY_FILE
from calculator import PortfolioCalculator
from data_handler import DataHandler
from plotter import PortfolioPlotter

def update_balance():
    """Основная функция обновления баланса"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Обновление баланса...")

    calculator = PortfolioCalculator(PORTFOLIO_FILE)
    data_handler = DataHandler(HISTORY_FILE)

    # Расчет баланса
    balance_data = calculator.calculate_total_balance()

    # Вывод в консоль
    print(f"\nОбщий баланс: {balance_data['total']:.2f} {balance_data['currency']}")
    print("-" * 50)

    for asset in balance_data['assets']:
        print(f"{asset['symbol']}: {asset['amount']:.6f} × {asset['price']:.2f} = "
              f"{asset['value']:.2f} {balance_data['currency']} ({asset['percentage']:.1f}%)")

    print("-" * 50)

    # Сохранение в историю
    if balance_data != 0:
        data_handler.save_balance_to_history(balance_data)
        print("Данные сохранены")
    else:
        print('Баланс 0, ОШИБКА')
        raise ValueError

    return balance_data

def show_portfolio():
    """Показать текущий портфель"""
    calculator = PortfolioCalculator(PORTFOLIO_FILE)

    print("\nТекущий портфель:")
    print("-" * 50)

    for asset in calculator.portfolio['assets']:
        print(f"{asset['symbol']}: {asset['amount']:.6f} - {asset.get('name', 'N/A')}")

    print("-" * 50)

def add_asset_interactive():
    """Интерактивное добавление актива"""
    calculator = PortfolioCalculator(PORTFOLIO_FILE)

    symbol = input("Введите символ криптовалюты (например, BTC): ").strip().upper()

    try:
        amount = float(input("Введите количество: "))
    except ValueError:
        print("Неверное количество")
        return

    name = input("Введите название (опционально): ").strip() or symbol
    is_stable = input("Это стейблкоин? (y/n): ").strip().lower() == 'y'

    calculator.add_asset(symbol, amount, name, is_stable)
    print(f"Добавлено: {amount} {symbol}")

def plot_history():
    """Построение графиков"""
    plotter = PortfolioPlotter(HISTORY_FILE)

    # График баланса
    plotter.plot_balance_history(days=7)

    # Расчет текущего баланса для круговой диаграммы
    calculator = PortfolioCalculator(PORTFOLIO_FILE)
    balance_data = calculator.calculate_total_balance()

    # Круговая диаграмма
    plotter.plot_pie_chart(balance_data)

def main():
    parser = argparse.ArgumentParser(description='Crypto Portfolio Tracker')
    parser.add_argument('--update', action='store_true', help='Обновить баланс')
    parser.add_argument('--show', action='store_true', help='Показать портфель')
    parser.add_argument('--add', action='store_true', help='Добавить актив')
    parser.add_argument('--plot', action='store_true', help='Построить графики')
    parser.add_argument('--auto', action='store_true', help='Автоматическое обновление каждые 30 минут')

    args = parser.parse_args()

    if args.update:
        update_balance()
    elif args.show:
        show_portfolio()
    elif args.add:
        add_asset_interactive()
    elif args.plot:
        plot_history()
    elif args.auto:
        print("Запуск автоматического обновления (каждые 30 минут)...")
        print("Нажмите Ctrl+C для остановки")

        # Первое обновление сразу
        update_balance()

        # Планировщик
        schedule.every(30).minutes.do(update_balance)

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Проверка каждую минуту
        except KeyboardInterrupt:
            print("\nОстановлено пользователем")
    else:
        # Интерактивный режим
        while True:
            print("\n" + "=" * 50)
            print("CRYPTO PORTFOLIO TRACKER")
            print("=" * 50)
            print("1. Обновить баланс")
            print("2. Показать портфель")
            print("3. Добавить актив")
            print("4. Построить графики")
            print("5. Автоматическое обновление (каждые 30 мин)")
            print("6. Выход")
            print("=" * 50)

            choice = input("Выберите действие (1-6): ").strip()

            if choice == '1':
                update_balance()
            elif choice == '2':
                show_portfolio()
            elif choice == '3':
                add_asset_interactive()
            elif choice == '4':
                plot_history()
            elif choice == '5':
                args.auto = True
                break
            elif choice == '6':
                print("Выход...")
                break
            else:
                print("Неверный выбор")

        if args.auto:
            # Запуск автоматического режима
            print("Запуск автоматического обновления (каждые 30 минут)...")
            print("Нажмите Ctrl+C для остановки")

            update_balance()

            schedule.every(30).minutes.do(update_balance)

            try:
                while True:
                    schedule.run_pending()
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\nОстановлено пользователем")

if __name__ == "__main__":
    main()