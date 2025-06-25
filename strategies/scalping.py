from __future__ import annotations

from collections import deque
from decimal import Decimal
from typing import Deque, List

from alpaca_bot.strategy.base import BaseStrategy, Signal


def _rsi(values: List[Decimal]) -> Decimal:
    """Compute a minimal RSI value for the provided closing prices."""
    gains = [max(Decimal(0), values[i] - values[i - 1]) for i in range(1, len(values))]
    losses = [max(Decimal(0), values[i - 1] - values[i]) for i in range(1, len(values))]
    avg_gain = sum(gains) / Decimal(len(gains))
    avg_loss = sum(losses) / Decimal(len(losses)) if sum(losses) > 0 else Decimal("1")
    rs = avg_gain / avg_loss
    return Decimal("100") - (Decimal("100") / (Decimal("1") + rs))


class MomentumScalper(BaseStrategy):
    """Scalping strategy combining momentum with RSI confirmation.

    This strategy attempts to capture very short-term moves. It keeps a deque of
    recent close prices so it can calculate a moving average and a simple RSI.
    A long signal is emitted when price is rising, above its short MA and the
    RSI shows strength. A short signal uses the opposite conditions.
    """

    def __init__(self, period: int = 5) -> None:
        self.period = period
        self.closes: Deque[Decimal] = deque(maxlen=period + 1)

    def _ma(self) -> Decimal:
        recent = list(self.closes)[-self.period :]
        return sum(recent) / Decimal(self.period)

    def on_bar(self, bar) -> List[Signal] | None:
        """Generate trading signals on each bar."""
        self.closes.append(bar.close)
        if len(self.closes) <= self.period:
            return None

        ma = self._ma()
        prev_close = list(self.closes)[-2]
        rsi = _rsi(list(self.closes)[-self.period - 1 :])

        if bar.close > prev_close and bar.close > ma and rsi > 55:
            # Strong upward momentum
            return [Signal("BUY", 10)]

        if bar.close < prev_close and bar.close < ma and rsi < 45:
            # Momentum to the downside
            return [Signal("SELL", 10)]

        return None
