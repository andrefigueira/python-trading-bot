from __future__ import annotations

from typing import Dict, Tuple


class DataCache:
    def __init__(self) -> None:
        self._bars: Dict[Tuple[str, str], list] = {}

    def add_bar(self, symbol: str, timeframe: str, bar: dict) -> None:
        self._bars.setdefault((symbol, timeframe), []).append(bar)

    def last_bar(self, symbol: str, timeframe: str) -> dict | None:
        bars = self._bars.get((symbol, timeframe))
        return bars[-1] if bars else None
