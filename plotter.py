import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta
import os

class PortfolioPlotter:
    def __init__(self, history_file):
        self.history_file = history_file

    def plot_balance_history(self, days=30):
        """Построение графика баланса за указанное количество дней"""
        try:
            df = pd.read_csv(self.history_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')

            # Фильтрация по дням
            if days:
                cutoff_date = datetime.now() - timedelta(days=days)
                df = df[df['timestamp'] > cutoff_date]

            if len(df) < 2:
                print("Недостаточно данных для построения графика")
                return

            # Создание графика
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})

            # Основной график баланса
            ax1.plot(df['timestamp'], df['total'], 'b-', linewidth=2, marker='o', markersize=4)
            ax1.set_title(f'Общий баланс портфеля ({df["currency"].iloc[0]})', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Баланс', fontsize=12)
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)

            # Форматирование оси времени
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))

            # График изменений
            df['change'] = df['total'].diff()
            colors = ['red' if x < 0 else 'green' for x in df['change']]
            ax2.bar(df['timestamp'], df['change'], color=colors, alpha=0.7)
            ax2.set_ylabel('Изменение', fontsize=12)
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))

            # Расчет статистики
            total_change = df['total'].iloc[-1] - df['total'].iloc[0]
            percent_change = (total_change / df['total'].iloc[0] * 100) if df['total'].iloc[0] > 0 else 0

            # Добавление статистики на график
            stats_text = f"Начало: {df['total'].iloc[0]:.2f} {df['currency'].iloc[0]}\n"
            stats_text += f"Текущий: {df['total'].iloc[-1]:.2f} {df['currency'].iloc[0]}\n"
            stats_text += f"Изменение: {total_change:+.2f} ({percent_change:+.2f}%)"

            ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

            plt.tight_layout()

            # Сохранение графика
            os.makedirs('charts', exist_ok=True)
            chart_file = f"charts/balance_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_file, dpi=150, bbox_inches='tight')
            plt.show()

            print(f"График сохранен как {chart_file}")

        except Exception as e:
            print(f"Ошибка при построении графика: {e}")

    def plot_pie_chart(self, balance_data):
        """Круговая диаграмма распределения активов"""
        assets = balance_data['assets']

        if not assets:
            print("Нет данных для построения диаграммы")
            return

        labels = [f"{a['symbol']}\n{a['percentage']:.1f}%" for a in assets]
        sizes = [a['value'] for a in assets]

        plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title(f'Распределение активов\nОбщий баланс: {balance_data["total"]:.2f} {balance_data["currency"]}')

        os.makedirs('charts', exist_ok=True)
        plt.savefig(f"charts/pie_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", dpi=150)
        plt.show()