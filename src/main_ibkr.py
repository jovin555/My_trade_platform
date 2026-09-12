from src.ibkr_broker import IBKRBroker
from src.config import Config


def main():
    broker = IBKRBroker()
    broker.connect()

    print(f"Connected to IB Gateway/TWS at {Config.IBKR_HOST}:{Config.IBKR_PORT}")
    for row in broker.get_account_summary():
        if row.tag in ('NetLiquidation', 'BuyingPower', 'TotalCashValue'):
            print(f"{row.tag}: {row.value} {row.currency}")

    broker.disconnect()


if __name__ == '__main__':
    main()
