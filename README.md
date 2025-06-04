# python-trading-bot

An async trading bot framework. See the [technical brief](docs/TECHNICAL_BRIEF.md) for architecture details.

## Quickstart (macOS)

1. Install Python 3.11 via Homebrew:

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

3. Install the package and optional web extras:

   ```bash
   pip install --editable .[web]
   ```

4. Initialise configuration:

   ```bash
   alpaca-bot init
   ```

   This creates `config.yaml` and `.env`. Populate `.env` with your Alpaca keys.

5. Edit `config.yaml` to choose symbols and strategies.

6. Run the bot:

   ```bash
   alpaca-bot run --mode paper
   ```

   Open `http://localhost:8000` for the dashboard (requires web extras).

### Adding strategies

Place Python files defining subclasses of `BaseStrategy` in `strategies/` and reference them under `strategies:` in `config.yaml`.

### Tests and coverage

Run the test suite with coverage:

```bash
pytest
```

For further information see the [technical brief](docs/TECHNICAL_BRIEF.md).
