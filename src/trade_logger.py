import json
from datetime import datetime, timezone
from pathlib import Path

DASHBOARD_DATA_DIR = Path(__file__).resolve().parent.parent / 'docs' / 'data'


class TradeLogger:
    def __init__(self, data_dir: Path = DASHBOARD_DATA_DIR):
        self.data_dir = data_dir
        self.trades_path = self.data_dir / 'trades.json'
        self.equity_path = self.data_dir / 'equity.json'
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _read(self, path: Path) -> list:
        if not path.exists():
            return []
        with open(path) as f:
            return json.load(f)

    def _write(self, path: Path, rows: list):
        with open(path, 'w') as f:
            json.dump(rows, f, indent=2)

    def log_trade(self, symbol: str, action: str, qty: float, price: float, currency: str = 'USD'):
        trades = self._read(self.trades_path)
        trades.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'symbol': symbol,
            'action': action,
            'qty': qty,
            'price': price,
            'currency': currency,
        })
        self._write(self.trades_path, trades)

    def log_equity(self, equity: float, currency: str):
        snapshots = self._read(self.equity_path)
        snapshots.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'equity': equity,
            'currency': currency,
        })
        self._write(self.equity_path, snapshots)
