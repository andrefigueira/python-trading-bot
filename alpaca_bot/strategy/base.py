from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List


class Signal:
    def __init__(self, side: str, qty_pct: float) -> None:
        self.side = side
        self.qty_pct = qty_pct


class BaseStrategy(ABC):
    indicators: Any

    @abstractmethod
    def on_bar(self, bar: Any) -> List[Signal] | None:
        raise NotImplementedError
