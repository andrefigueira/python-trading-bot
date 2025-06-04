import asyncio
import websockets
from alpaca_bot.brokers.alpaca.stream import AlpacaStream
from alpaca_bot.config import Settings


class DummyWS(websockets.WebSocketClientProtocol):
    def __init__(self, messages):
        super().__init__(messages)


def test_stream(monkeypatch):
    messages = ['{"t": "msg"}']

    async def fake_connect(url):
        return DummyWS(messages)

    monkeypatch.setattr(websockets, 'connect', fake_connect)
    stream = AlpacaStream(Settings())
    asyncio.run(stream.connect())

    received = []

    async def collect():
        async for msg in stream.listen():
            received.append(msg)
            break

    asyncio.run(collect())
    assert received == [{"t": "msg"}]
