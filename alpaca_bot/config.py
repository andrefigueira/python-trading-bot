from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import BaseModel, BaseSettings, Field


class AlpacaSettings(BaseModel):
    key_id: str = Field(..., env="ALPACA_KEY_ID")
    secret_key: str = Field(..., env="ALPACA_SECRET_KEY")
    base_url: str = "https://paper-api.alpaca.markets"


class StrategyConfig(BaseModel):
    name: str
    params: dict[str, int | float | str] | None = None


class ExecutionSettings(BaseModel):
    mode: str = "paper"  # live | paper | backtest
    symbols: List[str] = ["AAPL"]
    notional_max: int = 25000
    timezone: str = "America/New_York"


class RiskSettings(BaseModel):
    max_drawdown_pct: int = 10
    max_position_pct: int = 30
    min_equity_buffer_pct: int = 5


class Settings(BaseSettings):
    alpaca: AlpacaSettings = AlpacaSettings()
    execution: ExecutionSettings = ExecutionSettings()
    risk: RiskSettings = RiskSettings()
    strategies: List[StrategyConfig] = []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Settings":
        if path is None:
            path = Path("config.yaml")
        if Path(path).exists():
            return cls.parse_file(path)
        return cls()
