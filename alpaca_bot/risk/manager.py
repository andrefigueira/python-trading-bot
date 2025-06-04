from __future__ import annotations

from ..core.utils import get_logger


class RiskManager:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.logger = get_logger(self.__class__.__name__)

    def check_order(self, order) -> bool:
        # Placeholder implementation
        self.logger.info("risk check passed for %s", order)
        return True
