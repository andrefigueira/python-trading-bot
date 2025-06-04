from pathlib import Path

from typer.testing import CliRunner

from alpaca_bot.cli import app


def test_init(tmp_path: Path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "config.yaml"])
    assert result.exit_code == 0
    assert Path("config.yaml").exists()
    assert Path(".env").exists()
