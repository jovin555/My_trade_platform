import json
from datetime import date
from pathlib import Path

DEFAULT_STATE_PATH = Path(__file__).resolve().parent.parent / 'data' / 'risk_state.json'


class RiskManager:
    def __init__(self, max_position_pct: float, daily_loss_limit_pct: float,
                 daily_profit_target_pct: float = None,
                 weekly_profit_target_pct: float = None,
                 monthly_profit_target_pct: float = None,
                 state_path: Path = DEFAULT_STATE_PATH):
        self.max_position_pct = max_position_pct
        self.daily_loss_limit_pct = daily_loss_limit_pct
        self.daily_profit_target_pct = daily_profit_target_pct
        self.weekly_profit_target_pct = weekly_profit_target_pct
        self.monthly_profit_target_pct = monthly_profit_target_pct
        self.state_path = state_path

        self.day_key = None
        self.week_key = None
        self.month_key = None
        self.day_start_equity = None
        self.week_start_equity = None
        self.month_start_equity = None

        self._load_state()

    def _load_state(self):
        if not self.state_path.exists():
            return
        with open(self.state_path) as f:
            state = json.load(f)
        self.day_key = state.get('day_key')
        self.week_key = state.get('week_key')
        self.month_key = state.get('month_key')
        self.day_start_equity = state.get('day_start_equity')
        self.week_start_equity = state.get('week_start_equity')
        self.month_start_equity = state.get('month_start_equity')

    def _save_state(self):
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_path, 'w') as f:
            json.dump({
                'day_key': self.day_key,
                'week_key': self.week_key,
                'month_key': self.month_key,
                'day_start_equity': self.day_start_equity,
                'week_start_equity': self.week_start_equity,
                'month_start_equity': self.month_start_equity,
            }, f)

    def sync_periods(self, today: date, equity: float):
        """Roll the day/week/month equity anchors forward whenever the period changes.
        Persisted to disk so a bot restart mid-day/week/month doesn't reset progress
        toward a profit target or loss limit."""
        iso = today.isocalendar()
        day_key = today.isoformat()
        week_key = f'{iso.year}-W{iso.week:02d}'
        month_key = f'{today.year}-{today.month:02d}'

        changed = False
        if self.day_key != day_key:
            self.day_key, self.day_start_equity = day_key, equity
            changed = True
        if self.week_key != week_key:
            self.week_key, self.week_start_equity = week_key, equity
            changed = True
        if self.month_key != month_key:
            self.month_key, self.month_start_equity = month_key, equity
            changed = True
        if changed:
            self._save_state()

    @staticmethod
    def _pct_change(start, equity) -> float:
        if not start:
            return 0.0
        return (equity - start) / start

    def check_daily_loss(self, equity: float) -> bool:
        """Returns True if the daily loss limit has been breached."""
        return self._pct_change(self.day_start_equity, equity) <= -self.daily_loss_limit_pct

    def check_daily_profit_target(self, equity: float) -> bool:
        if self.daily_profit_target_pct is None:
            return False
        return self._pct_change(self.day_start_equity, equity) >= self.daily_profit_target_pct

    def check_weekly_profit_target(self, equity: float) -> bool:
        if self.weekly_profit_target_pct is None:
            return False
        return self._pct_change(self.week_start_equity, equity) >= self.weekly_profit_target_pct

    def check_monthly_profit_target(self, equity: float) -> bool:
        if self.monthly_profit_target_pct is None:
            return False
        return self._pct_change(self.month_start_equity, equity) >= self.monthly_profit_target_pct

    def position_size(self, buying_power: float, price: float) -> int:
        if price <= 0:
            return 0
        cap = buying_power * self.max_position_pct
        return int(cap // price)
