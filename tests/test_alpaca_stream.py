import asyncio
import websockets
from alpaca_bot.brokers.alpaca.stream import AlpacaStream
from alpaca_bot.config import Settings


class DummyWS:
    def __init__(self, messages):
        self.messages = messages
        self.sent = []

    async def send(self, msg):
        self.sent.append(msg)

    def __aiter__(self):
        async def iterator():
            for msg in self.messages:
                yield msg
        return iterator()


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


def test_listen_without_connect():
    stream = AlpacaStream(Settings())

    async def run():
        try:
            async for _ in stream.listen():
                pass
        except RuntimeError as e:
            return str(e)

    err = asyncio.run(run())
    assert err == "stream not connected"
