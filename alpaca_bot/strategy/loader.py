from __future__ import annotations

import importlib
from pathlib import Path
from typing import List, Type

from .base import BaseStrategy


def load_strategies(paths: List[str]) -> List[Type[BaseStrategy]]:
    strategies: List[Type[BaseStrategy]] = []
    for path in paths:
        module_name, _, class_name = path.rpartition(".")
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        if issubclass(cls, BaseStrategy):
            strategies.append(cls)
    return strategies


def discover(directory: str = "strategies") -> List[Type[BaseStrategy]]:
    strategies: List[Type[BaseStrategy]] = []
    for file in Path(directory).glob("*.py"):
        if file.stem.startswith("_"):
            continue
        mod = importlib.import_module(f"{directory}.{file.stem}")
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if isinstance(obj, type) and issubclass(obj, BaseStrategy) and obj is not BaseStrategy:
                strategies.append(obj)
    return strategies
