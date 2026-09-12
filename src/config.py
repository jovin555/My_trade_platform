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

    # IBKR (IB Gateway / TWS) — connection only, not a static API key.
    # Default ports: 4002 = Gateway paper, 4001 = Gateway live, 7497 = TWS paper, 7496 = TWS live.
    IBKR_HOST = os.getenv('IBKR_HOST', '127.0.0.1')
    IBKR_PORT = int(os.getenv('IBKR_PORT', '4002'))
    IBKR_CLIENT_ID = int(os.getenv('IBKR_CLIENT_ID', '1'))
