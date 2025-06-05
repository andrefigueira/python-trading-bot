from __future__ import annotations

from pathlib import Path

import typer
import yaml

from .config import Settings

DEFAULT_CONFIG = {
    "alpaca": {
        "key_id": "",
        "secret_key": "",
        "base_url": "https://paper-api.alpaca.markets",
    },
    "execution": {
        "mode": "paper",
        "symbols": ["AAPL"],
        "notional_max": 25000,
        "timezone": "America/New_York",
    },
    "risk": {
        "max_drawdown_pct": 10,
        "max_position_pct": 30,
        "min_equity_buffer_pct": 5,
    },
    "strategies": [],
}

app = typer.Typer(name="alpaca-bot")


@app.command()
def init(config_path: str = "config.yaml") -> None:
    """Create default config and .env files."""
    path = Path(config_path)
    path.write_text(yaml.safe_dump(DEFAULT_CONFIG, sort_keys=False))
    env = Path(".env")
    if not env.exists():
        env.write_text("ALPACA_KEY_ID=\nALPACA_SECRET_KEY=\n")
    typer.echo(f"created {path} and .env")


@app.command()
def run(
    mode: str = "paper",
    no_ui: bool = typer.Option(False, '--no-ui', help='Run without starting the web UI'),
) -> None:
    """Run the trading bot."""
    settings = Settings.load()
    typer.echo(
        f"running bot in {mode} mode with symbols {settings.execution.symbols}"
    )
    if not no_ui:
        import uvicorn

        uvicorn.run("alpaca_bot.web.api:app", host="0.0.0.0", port=8000)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
