import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
    ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
    ALPACA_PAPER = os.getenv('ALPACA_PAPER', 'true').lower() in ('1', 'true', 'yes')

    TICKERS = [t.strip() for t in os.getenv('TICKERS', 'AAPL,MSFT,NVDA,TSLA,AMZN').split(',') if t.strip()]
    RUN_INTERVAL_SECONDS = int(os.getenv('RUN_INTERVAL_SECONDS', '300'))
    MAX_POSITION_PCT = float(os.getenv('MAX_POSITION_PCT', '0.1'))
