from __future__ import annotations

from typing import List

from alpaca_bot.strategy.base import BaseStrategy, Signal


class MomentumScalper(BaseStrategy):
    """Scalp small moves by looking at bar direction."""

    def on_bar(self, bar) -> List[Signal] | None:
        if bar.close > bar.open:
            return [Signal("BUY", 10)]
        if bar.close < bar.open:
            return [Signal("SELL", 10)]
        return None
