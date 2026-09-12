import logging
import time
from datetime import datetime, time as dtime
from zoneinfo import ZoneInfo

from src.config import Config
from src.ibkr_broker import IBKRBroker
from src.risk import RiskManager
from src.trading_bot import TradingBot

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

MARKET_TZ = ZoneInfo('America/New_York')
MARKET_OPEN = dtime(9, 30)
MARKET_CLOSE = dtime(16, 0)


def is_market_open(now: datetime) -> bool:
    now = now.astimezone(MARKET_TZ)
    if now.weekday() >= 5:  # Saturday=5, Sunday=6
        return False
    return MARKET_OPEN <= now.time() <= MARKET_CLOSE


def main():
    logger.info('Starting live trading loop (TRADING_ENABLED=%s)', Config.TRADING_ENABLED)
    broker = IBKRBroker()
    broker.connect()
    risk = RiskManager(Config.MAX_POSITION_PCT, Config.DAILY_LOSS_LIMIT_PCT)
    bot = TradingBot(broker, risk)

    last_trading_day = None
    try:
        while True:
            now = datetime.now(MARKET_TZ)
            if is_market_open(now):
                if last_trading_day != now.date():
                    risk.start_new_day(broker.get_net_liquidation(Config.ACCOUNT_CURRENCY))
                    last_trading_day = now.date()
                    logger.info('New trading day %s — start equity %.2f %s', now.date(), risk.day_start_equity, Config.ACCOUNT_CURRENCY)
                bot.run_once()
            else:
                logger.info('Market closed (%s) — sleeping', now.strftime('%a %H:%M %Z'))
            time.sleep(Config.RUN_INTERVAL_SECONDS)
    finally:
        broker.disconnect()


if __name__ == '__main__':
    main()
