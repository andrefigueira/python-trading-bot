from __future__ import annotations

import asyncio
import json
import websockets

from ...config import Settings
from ...core.utils import get_logger


class AlpacaStream:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.logger = get_logger(self.__class__.__name__)
        self._ws_url = "wss://stream.data.alpaca.markets/v2/sip"
        self._connected = False
        self._conn: websockets.WebSocketClientProtocol | None = None

    async def connect(self) -> None:
        self._conn = await websockets.connect(self._ws_url)
        auth = {
            "action": "auth",
            "key": self.settings.alpaca.key_id,
            "secret": self.settings.alpaca.secret_key,
        }
        await self._conn.send(json.dumps(auth))
        self._connected = True
        self.logger.info("stream connected")

    async def listen(self) -> asyncio.AsyncIterator[dict]:
        if not self._conn:
            raise RuntimeError("stream not connected")
        async for msg in self._conn:
            yield json.loads(msg)
