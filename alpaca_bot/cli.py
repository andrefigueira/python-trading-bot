from __future__ import annotations

from pathlib import Path

import typer

from .config import Settings

app = typer.Typer(name="alpaca-bot")


@app.command()
def init(config_path: str = "config.yaml") -> None:
    """Create default config and .env files."""
    cfg = Settings()
    path = Path(config_path)
    path.write_text(cfg.json(indent=2))
    env = Path(".env")
    if not env.exists():
        env.write_text("ALPACA_KEY_ID=\nALPACA_SECRET_KEY=\n")
    typer.echo(f"created {path} and .env")


@app.command()
def run(mode: str = "paper") -> None:
    """Run the trading bot."""
    settings = Settings.load()
    typer.echo(f"running bot in {mode} mode with symbols {settings.execution.symbols}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
