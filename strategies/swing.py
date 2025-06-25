from __future__ import annotations

from collections import deque
from decimal import Decimal
from typing import Deque, List

from alpaca_bot.strategy.base import BaseStrategy, Signal


class SwingBreakout(BaseStrategy):
    """Swing trading strategy that buys breakouts and sells breakdowns."""

    def __init__(self, window: int = 5) -> None:
        self.window = window
        self.highs: Deque[Decimal] = deque(maxlen=window)
        self.lows: Deque[Decimal] = deque(maxlen=window)

    def on_bar(self, bar) -> List[Signal] | None:
        prev_highs = list(self.highs)
        prev_lows = list(self.lows)
        self.highs.append(bar.high)
        self.lows.append(bar.low)
        if len(prev_highs) < self.window:
            return None
        if bar.close > max(prev_highs):
            return [Signal("BUY", 100)]
        if bar.close < min(prev_lows):
            return [Signal("SELL", 100)]
        return None
