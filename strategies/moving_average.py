from __future__ import annotations

from collections import deque
from decimal import Decimal
from typing import Deque, List

from alpaca_bot.strategy.base import BaseStrategy, Signal


class MovingAverageCross(BaseStrategy):
    """Simple moving average crossover strategy."""

    def __init__(self, fast: int = 5, slow: int = 20) -> None:
        if fast >= slow:
            raise ValueError("fast period must be < slow period")
        self.fast = fast
        self.slow = slow
        self.prices: Deque[Decimal] = deque(maxlen=slow)

    def on_bar(self, bar) -> List[Signal] | None:
        self.prices.append(bar.close)
        if len(self.prices) < self.slow:
            return None
        fast_ma = sum(list(self.prices)[-self.fast:]) / Decimal(self.fast)
        slow_ma = sum(self.prices) / Decimal(self.slow)
        if fast_ma > slow_ma:
            return [Signal("BUY", 100)]
        elif fast_ma < slow_ma:
            return [Signal("SELL", 100)]
        return None
