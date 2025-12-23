import csv
import json
import pandas as pd
from datetime import datetime
import os

class DataHandler:
    def __init__(self, history_file):
        self.history_file = history_file

    def save_balance_to_history(self, balance_data):
        """Сохранение баланса в историю"""
        file_exists = os.path.isfile(self.history_file)

        with open(self.history_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'total', 'currency'
            ])

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'timestamp': balance_data['timestamp'],
                'total': balance_data['total'],
                'currency': balance_data['currency']
            })

        # Также сохраняем детальный снимок в JSON
        snapshot_file = f"snapshots/snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('snapshots', exist_ok=True)

        with open(snapshot_file, 'w') as f:
            json.dump(balance_data, f, indent=2)

    def get_historical_data(self):
        """Получение исторических данных"""
        try:
            df = pd.read_csv(self.history_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            return df
        except FileNotFoundError:
            return pd.DataFrame()