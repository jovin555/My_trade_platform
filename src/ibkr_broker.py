from ib_async import IB, Stock, MarketOrder

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

    def get_positions(self):
        return self.ib.positions()

    def submit_market_order(self, symbol: str, qty: float, action: str, currency: str = 'USD'):
        contract = Stock(symbol, 'SMART', currency)
        self.ib.qualifyContracts(contract)
        order = MarketOrder(action, qty)
        return self.ib.placeOrder(contract, order)
