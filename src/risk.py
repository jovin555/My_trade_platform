class RiskManager:
    def __init__(self, max_position_pct: float, daily_loss_limit_pct: float):
        self.max_position_pct = max_position_pct
        self.daily_loss_limit_pct = daily_loss_limit_pct
        self.day_start_equity = None
        self.halted = False

    def start_new_day(self, equity: float):
        self.day_start_equity = equity
        self.halted = False

    def check_daily_loss(self, equity: float) -> bool:
        """Returns True if the daily loss limit has been breached (and halts trading)."""
        if self.day_start_equity is None:
            self.start_new_day(equity)
            return False
        loss_pct = (self.day_start_equity - equity) / self.day_start_equity
        if loss_pct >= self.daily_loss_limit_pct:
            self.halted = True
        return self.halted

    def position_size(self, buying_power: float, price: float) -> int:
        if price <= 0:
            return 0
        cap = buying_power * self.max_position_pct
        return int(cap // price)
