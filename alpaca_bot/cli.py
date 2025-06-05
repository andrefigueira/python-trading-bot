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

PORTFOLIO = {"balance": 0.0, "pnl": 0.0}
ORDERS = {"open": [], "closed": [], "pending": []}


@app.command()
def init(config_path: str = "config.yaml") -> None:
    """Create default config and .env files."""
    path = Path(config_path)
    path.write_text(yaml.safe_dump(DEFAULT_CONFIG, sort_keys=False))
    env = Path(".env")
    if not env.exists():
        env.write_text(
            "\n".join(
                [
                    "ALPACA_KEY_ID=",
                    "ALPACA_SECRET_KEY=",
                    "ALPACA_BASE_URL=https://paper-api.alpaca.markets",
                    "EXECUTION_MODE=paper",
                    "EXECUTION_SYMBOLS=AAPL",
                    "EXECUTION_NOTIONAL_MAX=25000",
                    "EXECUTION_TIMEZONE=America/New_York",
                    "RISK_MAX_DRAWDOWN_PCT=10",
                    "RISK_MAX_POSITION_PCT=30",
                    "RISK_MIN_EQUITY_BUFFER_PCT=5",
                ]
            )
            + "\n"
        )
    typer.echo(f"created {path} and .env")


@app.command()
def run(mode: str = "paper") -> None:
    """Run the trading bot."""
    settings = Settings.load()
    typer.echo(
        f"running bot in {mode} mode with symbols {settings.execution.symbols}"
    )


@app.command("set-symbols")
def set_symbols(symbols: str) -> None:
    """Update trading symbols in config.yaml."""
    settings = Settings.load()
    parsed = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    settings.execution.symbols = parsed
    Path("config.yaml").write_text(
        yaml.safe_dump(settings.dict(), sort_keys=False)
    )
    typer.echo("symbols updated: " + ", ".join(parsed))


@app.command()
def portfolio() -> None:
    """Display portfolio balance and P&L."""
    typer.echo(f"Balance: {PORTFOLIO['balance']}")
    typer.echo(f"P&L: {PORTFOLIO['pnl']}")


@app.command()
def orders() -> None:
    """Show open, closed and pending orders."""
    for key, vals in ORDERS.items():
        typer.echo(key.capitalize() + ":")
        for val in vals:
            typer.echo(f"  - {val}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
