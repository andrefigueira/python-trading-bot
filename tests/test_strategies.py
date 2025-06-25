from datetime import datetime
from decimal import Decimal

from alpaca_bot.core.models import Bar
from strategies.moving_average import MovingAverageCross
from strategies.rsi_reversion import RSIReversion
from strategies.scalping import MomentumScalper
from strategies.swing import SwingBreakout
from strategies.composite import CompositeStrategy


def make_bar(open_price: float, close_price: float, high: float | None = None, low: float | None = None) -> Bar:
    high_val = Decimal(high if high is not None else max(open_price, close_price))
    low_val = Decimal(low if low is not None else min(open_price, close_price))
    return Bar(
        "AAPL",
        datetime(2024, 1, 1),
        Decimal(open_price),
        high_val,
        low_val,
        Decimal(close_price),
        100,
    )


def test_moving_average_cross():
    strat = MovingAverageCross(fast=2, slow=3)
    strat.on_bar(make_bar(1, 1))
    strat.on_bar(make_bar(2, 2))
    sigs = strat.on_bar(make_bar(3, 3))
    assert sigs and sigs[0].side == "BUY"
    sigs = strat.on_bar(make_bar(0, 0))
    assert sigs and sigs[0].side == "SELL"


def test_rsi_reversion():
    strat = RSIReversion(period=2)
    strat.on_bar(make_bar(3, 3))
    strat.on_bar(make_bar(2, 2))
    sigs = strat.on_bar(make_bar(1, 1))
    assert sigs and sigs[0].side == "BUY"

    strat = RSIReversion(period=2)
    strat.on_bar(make_bar(1, 1))
    strat.on_bar(make_bar(2, 2))
    sigs = strat.on_bar(make_bar(6, 6))

    assert sigs and sigs[0].side == "SELL"

def test_momentum_scalper():
    scalper = MomentumScalper(period=2)
    scalper.on_bar(make_bar(1, 1))
    scalper.on_bar(make_bar(2, 2))
    sigs = scalper.on_bar(make_bar(3, 3))
    assert sigs and sigs[0].side == "BUY"
    sigs = scalper.on_bar(make_bar(1, 1))
    assert sigs and sigs[0].side == "SELL"


def test_swing_breakout():
    swing = SwingBreakout(window=2, ma_period=3)
    swing.on_bar(make_bar(1, 1, high=1, low=1))
    swing.on_bar(make_bar(2, 2, high=2, low=2))
    sigs = swing.on_bar(make_bar(3, 3, high=3, low=3))
    assert sigs and sigs[0].side == "BUY"

    swing = SwingBreakout(window=2, ma_period=3)
    swing.on_bar(make_bar(3, 3, high=3, low=3))
    swing.on_bar(make_bar(2, 2, high=2, low=2))
    sigs = swing.on_bar(make_bar(1, 1, high=1, low=1))
    assert sigs and sigs[0].side == "SELL"


def test_composite_strategy():
    ma = MovingAverageCross(fast=2, slow=3)
    scalp = MomentumScalper(period=2)
    comp = CompositeStrategy([ma, scalp])
    comp.on_bar(make_bar(1, 1))
    comp.on_bar(make_bar(2, 2))
    sigs = comp.on_bar(make_bar(2, 3))
    assert len(sigs) == 2
