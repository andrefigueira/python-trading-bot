from __future__ import annotations

import httpx

from ...core.utils import get_logger
from ...config import Settings


class AlpacaClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.base_url = settings.alpaca.base_url
        self._client = httpx.AsyncClient(base_url=self.base_url)
        self.logger = get_logger(self.__class__.__name__)

    async def get_account(self) -> dict:
        resp = await self._client.get(
            "/v2/account",
            headers={
                "APCA-API-KEY-ID": self.settings.alpaca.key_id,
                "APCA-API-SECRET-KEY": self.settings.alpaca.secret_key,
            },
        )
        resp.raise_for_status()
        return resp.json()
