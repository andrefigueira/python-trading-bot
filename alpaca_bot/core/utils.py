from __future__ import annotations

import logging
from functools import wraps
from time import sleep
from typing import Any, Callable, TypeVar


T = TypeVar("T")


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
        )
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def retry(times: int = 3, delay: float = 1.0) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            exc: Exception | None = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # pragma: no cover - used as generic util
                    exc = e
                    sleep(delay)
            raise exc  # type: ignore

        return wrapper

    return decorator
