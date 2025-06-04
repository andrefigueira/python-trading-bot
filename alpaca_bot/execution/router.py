from __future__ import annotations

from ..core.utils import get_logger


class OrderRouter:
    def __init__(self, client) -> None:
        self.client = client
        self.logger = get_logger(self.__class__.__name__)

    async def submit(self, order) -> None:
        self.logger.info("submitting order %s", order)
        await self.client.submit_order(order)
