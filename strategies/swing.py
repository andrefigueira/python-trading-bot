from __future__ import annotations

from collections import deque
from decimal import Decimal
from typing import Deque, List

from alpaca_bot.strategy.base import BaseStrategy, Signal


class SwingBreakout(BaseStrategy):
    """Swing strategy buying breakouts with a trend filter."""

    def __init__(self, window: int = 5, ma_period: int = 20) -> None:
        self.window = window
        self.ma_period = ma_period
        self.highs: Deque[Decimal] = deque(maxlen=window)
        self.lows: Deque[Decimal] = deque(maxlen=window)
        self.closes: Deque[Decimal] = deque(maxlen=ma_period)

    def _ma(self) -> Decimal:
        recent = list(self.closes)[-self.ma_period :]
        return sum(recent) / Decimal(self.ma_period)

    def on_bar(self, bar) -> List[Signal] | None:
        prev_highs = list(self.highs)
        prev_lows = list(self.lows)
        self.highs.append(bar.high)
        self.lows.append(bar.low)
        self.closes.append(bar.close)
        if len(prev_highs) < self.window or len(self.closes) < self.ma_period:
            return None
        ma = self._ma()
        if bar.close > ma and bar.close > max(prev_highs):
            return [Signal("BUY", 100)]
        if bar.close < ma and bar.close < min(prev_lows):
            return [Signal("SELL", 100)]
        return None
