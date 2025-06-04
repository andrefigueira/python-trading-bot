from decimal import Decimal

from alpaca_bot.execution.router import OrderRouter
from alpaca_bot.execution.portfolio import Portfolio


class DummyClient:
    def __init__(self):
        self.orders = []

    async def submit_order(self, order):
        self.orders.append(order)


import asyncio


def test_order_router():
    client = DummyClient()
    router = OrderRouter(client)
    order = {'symbol': 'AAPL'}
    asyncio.run(router.submit(order))
    assert client.orders == [order]


def test_portfolio_update():
    pf = Portfolio()
    pf.update('AAPL', Decimal('1'))
    pf.update('AAPL', Decimal('2'))
    assert pf.positions['AAPL'] == Decimal('3')
