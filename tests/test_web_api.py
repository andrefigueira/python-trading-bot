from pathlib import Path

from fastapi.testclient import TestClient
import yaml

from alpaca_bot.web import api
from alpaca_bot.cli import DEFAULT_CONFIG

app = api.app


def test_health_endpoint():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.json() == {"status": "ok"}


def test_dashboard_and_update_symbols(tmp_path: Path, monkeypatch):
    config = tmp_path / "config.yaml"
    config.write_text(yaml.safe_dump(DEFAULT_CONFIG, sort_keys=False))
    monkeypatch.setattr(api, "CONFIG_PATH", config)
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Dashboard" in resp.text

    resp = client.post("/update_symbols", data={"symbols": "TSLA,AMZN"})
    assert resp.json()["symbols"] == ["TSLA", "AMZN"]
    data = yaml.safe_load(config.read_text())
    assert data["execution"]["symbols"] == ["TSLA", "AMZN"]
