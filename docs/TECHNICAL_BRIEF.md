################################################################################
# Python Alpaca Trading Bot – Full Technical Brief (SOLID, Performant, Secure) #
# Copy-paste this single block into Codex – it contains EVERYTHING.             #
################################################################################

0. TL;DR
--------
Ship an install-and-go Python package (`alpaca-bot`) that lets a user:
1. `pipx install alpaca-bot[web]`
2. `alpaca-bot init` → creates `config.yaml` + `.env`
3. Drop/modify strategy files in `strategies/`
4. `alpaca-bot run --mode paper|live` and monitor the web dashboard.

Design rules: SOLID, async-first, typed, secure key handling, 90 %+ test coverage.

1. Project Layout
-----------------
alpaca_bot/
├── __init__.py
├── cli.py                 Typer CLI, entry-point: `alpaca-bot`
├── config.py              Pydantic settings (Single Responsibility)
├── core/                  Broker-agnostic abstractions
│   ├── events.py          Async pub/sub bus
│   ├── models.py          Typed dataclasses (bars, orders, fills…)
│   └── utils.py           Retry, back-off, secrets, logging helpers
├── brokers/
│   └── alpaca/            Alpaca implementation (Open/Closed)
│       ├── client.py
│       └── stream.py
├── data/
│   ├── cache.py           In-memory + SQLite/Parquet persistence
│   └── backtester.py      Vectorised backtest engine
├── strategy/
│   ├── base.py            `BaseStrategy` ABC (Liskov-safe)
│   ├── loader.py          Hot-reload & DI of user plugins
│   └── indicators.py      TA helpers (numpy/numba-accelerated)
├── risk/
│   └── manager.py         Rule-driven risk checks
├── execution/
│   ├── router.py          Idempotent order placement
│   └── portfolio.py       Position & P&L tracker
├── web/
│   ├── api.py             FastAPI backend
│   └── ui/                React/HTMX SPA
└── tests/                 pytest, >90 % coverage

2. Key SOLID Mapping
--------------------
• SRP – each sub-package has one concern  
• OCP – new brokers/strategies via adapters/plugins  
• LSP – concrete strategies honour `BaseStrategy` contract  
• ISP – separate read-only market data vs trading write interfaces  
• DIP – high-level code depends on abstract `core.*` interfaces; implementations injected at runtime.

3. Security
-----------
• API keys only in `.env` or OS keyring (python-decouple).  
• LiteFS-backed encrypted SQLite for persisted state.  
• Minimal Alpaca key scopes.  
• HTTPS everywhere; TLS cert verification on.  
• Static analysis: bandit, safety, dependabot.

4. Performance & Reliability
----------------------------
• Fully async (`httpx`, `websockets`, `uvicorn`).  
• Vectorised numpy/numba indicators.  
• Order router uses idempotency keys & bulk submission.  
• LRU cache for recent bars, Parquet for archival.  
• Automatic reconnect with exponential back-off.  
• JSON logs + Prometheus metrics (`/metrics`).

5. Quickstart (README excerpt)
------------------------------
pipx install "alpaca-bot[web]"  
alpaca-bot init  
alpaca-bot run --mode paper  
open http://localhost:8000  

6. Example config.yaml
----------------------
alpaca:
  key_id:      "${ALPACA_KEY_ID}"
  secret_key:  "${ALPACA_SECRET_KEY}"
  base_url:    "https://paper-api.alpaca.markets"

execution:
  mode:         paper        # live | paper | backtest
  symbols:      ["AAPL", "MSFT", "NVDA"]
  notional_max: 25000
  timezone:     "America/New_York"

risk:
  max_drawdown_pct:      10
  max_position_pct:      30
  min_equity_buffer_pct: 5

strategies:
  - name: sma_cross.SmaCross
    params:
      fast: 10
      slow: 30

7. Strategy Plugin Skeleton (strategies/sma_cross.py)
-----------------------------------------------------
from alpaca_bot.strategy import BaseStrategy, Signal

class SmaCross(BaseStrategy):
    """Simple moving-average crossover demo."""
    fast: int = 10
    slow: int = 30

    def on_bar(self, bar) -> list[Signal] | None:
        fast_ma = self.indicators.SMA(self.fast)
        slow_ma = self.indicators.SMA(self.slow)
        if fast_ma.crosses_above(slow_ma):
            return [Signal("BUY", qty_pct=0.25)]
        if fast_ma.crosses_below(slow_ma):
            return [Signal("SELL", qty_pct=0.25)]

8. Testing & CI
---------------
• pytest-asyncio; faker fixtures; Alpaca sandbox.  
• GitHub Actions: ruff → mypy → bandit → pytest → coverage gate >90 %.  
• Pre-commit hooks enforce formatting (black), imports (isort), security (bandit).

9. Packaging & Deployment
-------------------------
• pyproject.toml (Poetry), semver tags.  
• Docker image: `ghcr.io/org/alpaca-bot:latest`.  
• `alpaca-bot service install --systemd` or pm2.  
• Helm chart scaffold under `deploy/helm`.

10. Stretch Goals
-----------------
• Multiple broker adapters (IBKR, Binance).  
• Strategy marketplace with sandboxing.  
• Jupyter live-notebook integration.  
• Regime-aware risk engine (kNN).

################################################################################
# END – this single block is ready for Codex.                                  #
################################################################################
