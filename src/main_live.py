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
    risk = RiskManager(
        Config.MAX_POSITION_PCT,
        Config.DAILY_LOSS_LIMIT_PCT,
        daily_profit_target_pct=Config.DAILY_PROFIT_TARGET_PCT,
        weekly_profit_target_pct=Config.WEEKLY_PROFIT_TARGET_PCT,
        monthly_profit_target_pct=Config.MONTHLY_PROFIT_TARGET_PCT,
    )
    bot = TradingBot(broker, risk)

    try:
        while True:
            now = datetime.now(MARKET_TZ)
            if is_market_open(now):
                bot.run_once(now)
            else:
                logger.info('Market closed (%s) — sleeping', now.strftime('%a %H:%M %Z'))
            time.sleep(Config.RUN_INTERVAL_SECONDS)
    finally:
        broker.disconnect()


if __name__ == '__main__':
    main()
