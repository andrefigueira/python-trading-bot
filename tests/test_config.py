from pathlib import Path

from alpaca_bot.config import Settings


def test_default_load(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    s = Settings.load()
    assert s.alpaca.base_url.startswith("https://")
