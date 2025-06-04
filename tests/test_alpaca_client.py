import asyncio
from alpaca_bot.brokers.alpaca.client import AlpacaClient
from alpaca_bot.config import Settings


def test_get_account():
    async def run():
        client = AlpacaClient(Settings())
        return await client.get_account()

    resp = asyncio.run(run())
    assert resp == {'account': 'ok'}
