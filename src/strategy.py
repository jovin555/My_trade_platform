import pandas as pd


def sma_crossover_signal(closes: pd.Series, fast: int, slow: int) -> str:
    """Return 'BUY', 'SELL', or 'HOLD' based on the latest fast/slow SMA crossover."""
    if len(closes) < slow + 1:
        return 'HOLD'

    fast_sma = closes.rolling(fast).mean()
    slow_sma = closes.rolling(slow).mean()

    prev_diff = fast_sma.iloc[-2] - slow_sma.iloc[-2]
    curr_diff = fast_sma.iloc[-1] - slow_sma.iloc[-1]

    if prev_diff <= 0 < curr_diff:
        return 'BUY'
    if prev_diff >= 0 > curr_diff:
        return 'SELL'
    return 'HOLD'
