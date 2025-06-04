import sys
from alpaca_bot.strategy.loader import discover


def test_discover(tmp_path, monkeypatch):
    pkg = tmp_path / 'pkg'
    pkg.mkdir()
    (pkg / '__init__.py').write_text('')
    strategy_file = pkg / 's.py'
    strategy_file.write_text('from alpaca_bot.strategy.base import BaseStrategy\nclass S(BaseStrategy):\n    def on_bar(self, bar):\n        return None\n')
    sys.path.insert(0, str(tmp_path))
    monkeypatch.chdir(tmp_path)
    strategies = discover('pkg')
    sys.path.pop(0)
    names = [s.__name__ for s in strategies]
    assert 'S' in names
