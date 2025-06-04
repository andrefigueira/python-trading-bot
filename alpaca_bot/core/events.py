from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, Awaitable, Callable, DefaultDict, List

EventHandler = Callable[[Any], Awaitable[None]]


class EventBus:
    def __init__(self) -> None:
        self._subs: DefaultDict[str, List[EventHandler]] = defaultdict(list)

    def subscribe(self, event: str, handler: EventHandler) -> None:
        self._subs[event].append(handler)

    async def publish(self, event: str, payload: Any) -> None:
        handlers = list(self._subs.get(event, []))
        await asyncio.gather(*(h(payload) for h in handlers))
