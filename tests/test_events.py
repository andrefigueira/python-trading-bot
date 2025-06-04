import asyncio
from alpaca_bot.core.events import EventBus


def test_event_bus():
    bus = EventBus()
    received = []

    async def handler(payload):
        received.append(payload)

    bus.subscribe('tick', handler)
    asyncio.run(bus.publish('tick', 123))
    assert received == [123]
