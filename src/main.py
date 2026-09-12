from src.broker import Broker
from src.config import Config


def main():
    broker = Broker()
    account = broker.get_account()

    print(f"Connected to Alpaca ({'paper' if Config.ALPACA_PAPER else 'live'} trading)")
    print(f"Account status: {account.status}")
    print(f"Buying power: {account.buying_power}")
    print(f"Watchlist: {', '.join(Config.TICKERS)}")


if __name__ == '__main__':
    main()
