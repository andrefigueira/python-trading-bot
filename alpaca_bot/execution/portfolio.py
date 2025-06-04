from __future__ import annotations

from decimal import Decimal
from typing import Dict


class Portfolio:
    def __init__(self) -> None:
        self.positions: Dict[str, Decimal] = {}

    def update(self, symbol: str, qty: Decimal) -> None:
        self.positions[symbol] = self.positions.get(symbol, Decimal("0")) + qty
