import logging

from src.config import Config
from src.ibkr_broker import IBKRBroker
from src.risk import RiskManager
from src.strategy import sma_crossover_signal

logger = logging.getLogger(__name__)


class TradingBot:
    def __init__(self, broker: IBKRBroker, risk: RiskManager):
        self.broker = broker
        self.risk = risk

    def _current_qty(self, symbol: str) -> float:
        for pos in self.broker.get_positions():
            if pos.contract.symbol == symbol:
                return pos.position
        return 0

    def _any_position_open(self) -> bool:
        return any(pos.position != 0 for pos in self.broker.get_positions())

    def run_once(self):
        equity_account_ccy = self.broker.get_net_liquidation(Config.ACCOUNT_CURRENCY)
        if self.risk.check_daily_loss(equity_account_ccy):
            logger.warning('Daily loss limit breached (%.2f -> %.2f %s) — trading halted for today', self.risk.day_start_equity, equity_account_ccy, Config.ACCOUNT_CURRENCY)
            return

        # Tickers trade in USD; convert account equity so position sizing compares
        # like-for-like against USD share prices instead of treating 1 CAD == 1 USD.
        fx_rate = self.broker.get_fx_rate('USD', Config.ACCOUNT_CURRENCY)
        equity_usd = equity_account_ccy / fx_rate

        # MAX_POSITION_PCT is sized against current equity per-signal, not a running
        # allocation — with a small account and high position pct, only one position
        # should be open at a time or later buys would overspend/fail.
        position_open = self._any_position_open()

        for symbol in Config.TICKERS:
            closes = self.broker.get_daily_closes(symbol)
            signal = sma_crossover_signal(closes, Config.SMA_FAST, Config.SMA_SLOW)
            qty_held = self._current_qty(symbol)

            if signal == 'BUY' and qty_held == 0 and position_open:
                logger.info('%s: BUY signal but a position is already open elsewhere — skipping', symbol)
                continue

            if signal == 'BUY' and qty_held == 0:
                price = closes.iloc[-1]
                qty = self.risk.position_size(equity_usd, price)
                if qty <= 0:
                    logger.info('%s: BUY signal but position size rounds to 0 (equity_usd=%.2f, price=%.2f)', symbol, equity_usd, price)
                    continue
                logger.info('%s: BUY signal, qty=%d', symbol, qty)
                if Config.TRADING_ENABLED:
                    self.broker.submit_market_order(symbol, qty, 'BUY')
                    position_open = True
                else:
                    logger.info('%s: TRADING_ENABLED=false — order not sent (dry run)', symbol)

            elif signal == 'SELL' and qty_held > 0:
                logger.info('%s: SELL signal, qty=%d', symbol, qty_held)
                if Config.TRADING_ENABLED:
                    self.broker.submit_market_order(symbol, qty_held, 'SELL')
                else:
                    logger.info('%s: TRADING_ENABLED=false — order not sent (dry run)', symbol)
            else:
                logger.info('%s: signal=%s, qty_held=%s — no action', symbol, signal, qty_held)
