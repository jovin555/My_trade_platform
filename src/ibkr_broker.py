import pandas as pd
from ib_async import IB, Stock, Forex, MarketOrder

from src.config import Config


class IBKRBroker:
    def __init__(self):
        self.ib = IB()

    def connect(self):
        self.ib.connect(Config.IBKR_HOST, Config.IBKR_PORT, clientId=Config.IBKR_CLIENT_ID)
        return self.ib

    def disconnect(self):
        self.ib.disconnect()

    def get_account_summary(self):
        return self.ib.accountSummary()

    def get_net_liquidation(self, currency: str) -> float:
        for row in self.ib.accountSummary():
            if row.tag == 'NetLiquidation' and row.currency == currency:
                return float(row.value)
        raise ValueError(f'NetLiquidation in {currency} not found in account summary')

    def get_positions(self):
        return self.ib.positions()

    def get_fx_rate(self, base: str, quote: str) -> float:
        """1 unit of `base` in `quote` currency, e.g. get_fx_rate('USD', 'CAD') -> ~1.38."""
        if base == quote:
            return 1.0
        contract = Forex(base + quote)
        self.ib.qualifyContracts(contract)
        bars = self.ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='2 D',
            barSizeSetting='1 day',
            whatToShow='MIDPOINT',
            useRTH=False,
        )
        return bars[-1].close

    def get_daily_closes(self, symbol: str, currency: str = 'USD', lookback_days: int = 90) -> pd.Series:
        contract = Stock(symbol, 'SMART', currency)
        self.ib.qualifyContracts(contract)
        bars = self.ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr=f'{lookback_days} D',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=True,
        )
        return pd.Series([b.close for b in bars], index=[b.date for b in bars], name=symbol)

    def submit_market_order(self, symbol: str, qty: float, action: str, currency: str = 'USD'):
        contract = Stock(symbol, 'SMART', currency)
        self.ib.qualifyContracts(contract)
        order = MarketOrder(action, qty)
        return self.ib.placeOrder(contract, order)
