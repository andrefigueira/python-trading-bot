from alpaca_bot.risk.manager import RiskManager
from alpaca_bot.config import Settings


def test_risk_manager():
    rm = RiskManager(Settings())
    assert rm.check_order({'id': 1}) is True
