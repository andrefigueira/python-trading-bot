import asyncio

from alpaca_bot.web.api import app


async def call_health():
    handler = app.routes['/health']
    return await handler()


def test_health_endpoint():
    result = asyncio.run(call_health())
    assert result == {'status': 'ok'}
