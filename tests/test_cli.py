from pathlib import Path

from typer.testing import CliRunner
import yaml

from alpaca_bot.cli import app


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


def test_run_invokes_uvicorn(monkeypatch):
    runner = CliRunner()
    import uvicorn

    called = {"flag": False}

    def fake_run(*args, **kwargs):
        called["flag"] = True

    monkeypatch.setattr(uvicorn, "run", fake_run)
    result = runner.invoke(app, ["run"])
    assert result.exit_code == 0
    assert called["flag"] is True
