from __future__ import annotations

from collections import deque
from decimal import Decimal
from typing import Deque, List

from alpaca_bot.strategy.base import BaseStrategy, Signal


def _rsi(values: List[Decimal]) -> Decimal:
    """Compute RSI for the given closing prices."""
    gains = [max(Decimal(0), values[i] - values[i - 1]) for i in range(1, len(values))]
    losses = [max(Decimal(0), values[i - 1] - values[i]) for i in range(1, len(values))]
    avg_gain = sum(gains) / Decimal(len(gains))
    avg_loss = sum(losses) / Decimal(len(losses)) if sum(losses) > 0 else Decimal("1")
    rs = avg_gain / avg_loss
    return Decimal("100") - (Decimal("100") / (Decimal("1") + rs))


class SwingBreakout(BaseStrategy):
    """Swing breakout strategy with trend and momentum confirmation.

    The strategy looks for a break above the recent high (or below the recent
    low) while the price is trending in that direction. A moving average is used
    for trend confirmation and RSI helps avoid overbought/oversold entries.
    """

    def __init__(self, window: int = 5, ma_period: int = 20, rsi_period: int = 14) -> None:
        self.window = window
        self.ma_period = ma_period
        self.rsi_period = rsi_period
        size = max(ma_period, rsi_period) + 1
        self.highs: Deque[Decimal] = deque(maxlen=window)
        self.lows: Deque[Decimal] = deque(maxlen=window)
        self.closes: Deque[Decimal] = deque(maxlen=size)

    def _ma(self) -> Decimal:
        recent = list(self.closes)[-self.ma_period :]
        return sum(recent) / Decimal(self.ma_period)

    def _rsi(self) -> Decimal:
        recent = list(self.closes)[-self.rsi_period - 1 :]
        return _rsi(recent)

    def on_bar(self, bar) -> List[Signal] | None:
        prev_highs = list(self.highs)
        prev_lows = list(self.lows)
        self.highs.append(bar.high)
        self.lows.append(bar.low)
        self.closes.append(bar.close)

        if len(prev_highs) < self.window or len(self.closes) <= max(self.ma_period, self.rsi_period):
            return None

        ma = self._ma()
        rsi = self._rsi()

        if bar.close > ma and bar.close > max(prev_highs) and rsi > 60:
            # Breakout to the upside with momentum
            return [Signal("BUY", 100)]

        if bar.close < ma and bar.close < min(prev_lows) and rsi < 40:
            # Breakdown to the downside with weakness
            return [Signal("SELL", 100)]

        return None
