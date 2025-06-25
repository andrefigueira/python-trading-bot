from __future__ import annotations

from typing import Iterable, List

from alpaca_bot.strategy.base import BaseStrategy, Signal


class CompositeStrategy(BaseStrategy):
    """Combine multiple strategies and merge their signals."""

    def __init__(self, strategies: Iterable[BaseStrategy]) -> None:
        self.strategies = list(strategies)

    def on_bar(self, bar) -> List[Signal] | None:
        signals: List[Signal] = []
        for strat in self.strategies:
            res = strat.on_bar(bar)
            if res:
                signals.extend(res)
        return signals or None
