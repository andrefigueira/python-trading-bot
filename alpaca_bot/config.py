from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AlpacaSettings(BaseSettings):
    key_id: str = Field(default="")
    secret_key: str = Field(default="")
    base_url: str = "https://paper-api.alpaca.markets"

    model_config = SettingsConfigDict(env_prefix="ALPACA_")


class StrategyConfig(BaseModel):
    name: str
    params: dict[str, int | float | str] | None = None


class ExecutionSettings(BaseSettings):
    mode: str = "paper"  # live | paper | backtest
    symbols: List[str] = ["AAPL"]
    notional_max: int = 25000
    timezone: str = "America/New_York"

    model_config = SettingsConfigDict(env_prefix="EXECUTION_")


class RiskSettings(BaseSettings):
    max_drawdown_pct: int = 10
    max_position_pct: int = 30
    min_equity_buffer_pct: int = 5

    model_config = SettingsConfigDict(env_prefix="RISK_")


class Settings(BaseSettings):
    alpaca: AlpacaSettings = Field(default_factory=AlpacaSettings)
    execution: ExecutionSettings = Field(default_factory=ExecutionSettings)
    risk: RiskSettings = Field(default_factory=RiskSettings)
    strategies: List[StrategyConfig] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Settings":
        if path is None:
            path = Path("config.yaml")

        import yaml

        data: dict = {}
        if Path(path).exists():
            data = yaml.safe_load(Path(path).read_text()) or {}

        # load environment variables from .env and OS
        env_settings = cls()
        yaml_settings = cls.model_validate(data)

        def apply_env(env_obj: BaseModel, target_obj: BaseModel) -> None:
            for name, field in env_obj.__class__.model_fields.items():
                env_val = getattr(env_obj, name)
                tgt_val = getattr(target_obj, name)
                if isinstance(env_val, BaseModel):
                    apply_env(env_val, tgt_val)
                    setattr(target_obj, name, tgt_val)
                else:
                    if name in getattr(env_obj, "model_fields_set", set()):
                        setattr(target_obj, name, env_val)

        apply_env(env_settings, yaml_settings)
        return yaml_settings
