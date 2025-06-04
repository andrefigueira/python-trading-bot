pytest_plugins = ['pytest_cov']

import pytest

@pytest.fixture(autouse=True)
def alpaca_env(monkeypatch):
    monkeypatch.setenv('ALPACA_KEY_ID', 'key')
    monkeypatch.setenv('ALPACA_SECRET_KEY', 'secret')
