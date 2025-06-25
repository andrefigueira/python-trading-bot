# An opensourced bot programmed in python for trading.

## Running tests with coverage

Install the development dependencies and run the test suite to generate a
coverage report. The `pyproject.toml` configuration already enables the
`pytest-cov` plugin to collect coverage for the `alpaca_bot` package.

```bash
pip install -e .[dev]
pytest
```

An async trading bot framework. See the [technical brief](docs/TECHNICAL_BRIEF.md) for architecture details.

## Requirements

* Python 3.11 or newer must be installed. The `pyproject.toml` specifies
  `requires-python = ">=3.11"` so earlier versions will fail during `make setup`.

## Quickstart (macOS)

1. Install Python 3.11 or newer via Homebrew:

   ```bash
   brew install python@3.11
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Windows: `.venv\\Scripts\\activate`
   
   Linux: `source .venv/bin/activate`

3. Install the package:

   ```bash
   pip install --editable .
   ```

4. Initialise configuration:

   ```bash
   alpaca-bot init
   ```

   This creates `config.yaml` and `.env`. Populate `.env` with your Alpaca keys
   or any other settings (e.g. `EXECUTION_MODE=live`). Environment variables
   override values in `config.yaml`.

5. Edit `config.yaml` to choose symbols and strategies.

6. Run the bot:

   ```bash
   alpaca-bot run --mode paper
   ```

   The web dashboard starts automatically at `http://localhost:8000`. Pass
   `--no-ui` to disable it.

   Use additional commands like `alpaca-bot set-symbols "AAPL,MSFT"` to update
   trading symbols. `alpaca-bot portfolio` shows the current balance and P&L,
   while `alpaca-bot orders` lists open, closed and pending orders.
   Launch `alpaca-bot tui` for an interactive text interface.

## Using the Makefile

A `Makefile` automates common tasks:

```bash
make setup  # create virtual environment and install dependencies
make run    # run the bot
make test   # run the tests
make lint   # run the Ruff linter
```

### Adding strategies

Place Python files defining subclasses of `BaseStrategy` in `strategies/` and reference them under `strategies:` in `config.yaml`.
This repository provides several example strategies ready to use:

* `strategies.moving_average.MovingAverageCross` – simple moving average crossover
* `strategies.rsi_reversion.RSIReversion` – buys when RSI is oversold and sells when overbought
* `strategies.scalping.MomentumScalper` – uses a short-term moving average to scalp momentum
* `strategies.swing.SwingBreakout` – breakout strategy with a trend filter for swing trades
* `strategies.composite.CompositeStrategy` – combine multiple strategies together

Use them in your `config.yaml` like so:

```yaml
strategies:
  - name: strategies.moving_average.MovingAverageCross
    params: {fast: 5, slow: 20}
  - name: strategies.rsi_reversion.RSIReversion
    params: {period: 14}
  - name: strategies.scalping.MomentumScalper
    params: {period: 5}
```

### Tests and coverage

Run the test suite with coverage:

```bash
pytest
```

For further information see the [technical brief](docs/TECHNICAL_BRIEF.md).