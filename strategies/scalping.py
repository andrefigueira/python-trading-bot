from __future__ import annotations

from collections import deque
from decimal import Decimal
from typing import Deque, List

from alpaca_bot.strategy.base import BaseStrategy, Signal


class MomentumScalper(BaseStrategy):
    """Scalp short-term momentum using a moving average filter."""

    def __init__(self, period: int = 5) -> None:
        self.period = period
        self.closes: Deque[Decimal] = deque(maxlen=period + 1)

    def _ma(self) -> Decimal:
        recent = list(self.closes)[-self.period :]
        return sum(recent) / Decimal(self.period)

    def on_bar(self, bar) -> List[Signal] | None:
        self.closes.append(bar.close)
        if len(self.closes) <= self.period:
            return None
        ma = self._ma()
        prev_close = list(self.closes)[-2]
        if bar.close > prev_close and bar.close > ma:
            return [Signal("BUY", 10)]
        if bar.close < prev_close and bar.close < ma:
            return [Signal("SELL", 10)]
        return None
