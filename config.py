import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

FIAT_CURRENCY = 'USDT'

PORTFOLIO_FILE = 'portfolio.json'
HISTORY_FILE = "balance_history.csv"