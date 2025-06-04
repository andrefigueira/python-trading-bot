from datetime import datetime
from decimal import Decimal

from alpaca_bot.core.models import Bar, Order, Fill


def test_models():
    bar = Bar('AAPL', datetime(2024, 1, 1), Decimal('1'), Decimal('2'), Decimal('0.5'), Decimal('1.5'), 100)
    assert bar.symbol == 'AAPL'

    order = Order('1', 'AAPL', 'BUY', Decimal('10'))
    assert order.filled_qty == Decimal('0')

    fill = Fill('1', datetime(2024, 1, 1), Decimal('1.2'), Decimal('10'))
    assert fill.price == Decimal('1.2')
