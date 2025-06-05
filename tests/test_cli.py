from pathlib import Path

from typer.testing import CliRunner
import yaml

from alpaca_bot.cli import app, DEFAULT_CONFIG


def test_init(tmp_path: Path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)
    called = {"flag": False}
    original_safe_dump = yaml.safe_dump

    def spy_safe_dump(*args, **kwargs):
        called["flag"] = True
        return original_safe_dump(*args, **kwargs)

    monkeypatch.setattr(yaml, "safe_dump", spy_safe_dump)

    result = runner.invoke(app, ["init", "--config-path", "config.yaml"])
    assert result.exit_code == 0
    assert called["flag"] is True
    assert Path("config.yaml").exists()
    assert Path(".env").exists()

    # Ensure the config file contains valid YAML
    data = yaml.safe_load(Path("config.yaml").read_text())
    assert isinstance(data, dict)
    assert "alpaca" in data or data != {}


def test_set_symbols(tmp_path: Path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)
    Path("config.yaml").write_text(yaml.safe_dump(DEFAULT_CONFIG, sort_keys=False))
    result = runner.invoke(app, ["set-symbols", "TSLA,AMZN"])
    assert result.exit_code == 0
    data = yaml.safe_load(Path("config.yaml").read_text())
    assert data["execution"]["symbols"] == ["TSLA", "AMZN"]


def test_portfolio_and_orders_commands():
    runner = CliRunner()
    result = runner.invoke(app, ["portfolio"])
    assert "Balance:" in result.output
    result = runner.invoke(app, ["orders"])
    assert "Open:" in result.output
