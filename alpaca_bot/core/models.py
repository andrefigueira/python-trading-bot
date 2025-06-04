from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal


@dataclass(slots=True)
class Bar:
    symbol: str
    time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


@dataclass(slots=True)
class Order:
    id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    qty: Decimal
    filled_qty: Decimal = Decimal("0")


@dataclass(slots=True)
class Fill:
    order_id: str
    timestamp: datetime
    price: Decimal
    qty: Decimal
