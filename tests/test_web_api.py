from fastapi.testclient import TestClient
from alpaca_bot.web.api import app


def test_health_endpoint():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.json() == {"status": "ok"}
