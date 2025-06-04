import asyncio
import httpx
from alpaca_bot.brokers.alpaca.client import AlpacaClient
from alpaca_bot.config import Settings


def test_get_account(monkeypatch):
    async def fake_get(self, url, headers=None):
        request = httpx.Request("GET", url)
        return httpx.Response(status_code=200, json={"account": "ok"}, request=request)

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

    async def run():
        client = AlpacaClient(Settings())
        return await client.get_account()

    resp = asyncio.run(run())
    assert resp == {"account": "ok"}
