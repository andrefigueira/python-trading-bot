from pathlib import Path

from typer.testing import CliRunner
import yaml

from alpaca_bot.cli import app


def test_init(tmp_path: Path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "config.yaml"])
    assert result.exit_code == 0
    assert Path("config.yaml").exists()
    assert Path(".env").exists()

    # Ensure the config file contains valid YAML
    data = yaml.safe_load(Path("config.yaml").read_text())
    assert isinstance(data, dict)
    assert "alpaca" in data or data != {}
