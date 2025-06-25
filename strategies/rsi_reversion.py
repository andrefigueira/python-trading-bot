from __future__ import annotations

from collections import deque
from decimal import Decimal
from typing import Deque, List

from alpaca_bot.strategy.base import BaseStrategy, Signal


def _rsi(values: List[Decimal]) -> Decimal:
    gains = [max(Decimal(0), values[i] - values[i - 1]) for i in range(1, len(values))]
    losses = [max(Decimal(0), values[i - 1] - values[i]) for i in range(1, len(values))]
    avg_gain = sum(gains) / Decimal(len(gains))
    avg_loss = sum(losses) / Decimal(len(losses)) if sum(losses) > 0 else Decimal('1')
    rs = avg_gain / avg_loss
    return Decimal('100') - (Decimal('100') / (Decimal('1') + rs))


class RSIReversion(BaseStrategy):
    """Buy when RSI < 30, sell when RSI > 70."""

    def __init__(self, period: int = 14) -> None:
        self.period = period
        self.prices: Deque[Decimal] = deque(maxlen=period + 1)

    def on_bar(self, bar) -> List[Signal] | None:
        self.prices.append(bar.close)
        if len(self.prices) <= self.period:
            return None
        rsi = _rsi(list(self.prices))
        if rsi < 30:
            return [Signal("BUY", 100)]
        if rsi > 70:
            return [Signal("SELL", 100)]
        return None
