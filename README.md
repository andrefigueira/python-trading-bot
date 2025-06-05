# An opensourced bot programmed in python for trading.

## Running tests with coverage

Run the test suite with Poetry to automatically generate a coverage report. The `pyproject.toml`
configuration enables the `pytest-cov` plugin to collect coverage for the `alpaca_bot` package.

```bash
poetry run pytest
```
=======

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

   Use additional commands like `alpaca-bot set-symbols "AAPL,MSFT"` to update
   trading symbols. `alpaca-bot portfolio` shows the current balance and P&L,
   while `alpaca-bot orders` lists open, closed and pending orders.

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

### Tests and coverage

Run the test suite with coverage:

```bash
pytest
```

For further information see the [technical brief](docs/TECHNICAL_BRIEF.md).