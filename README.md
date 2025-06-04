# python-trading-bot
An opensourced bot programmed in python for trading.

## Installation
```bash
pip install -e .
```

## Usage
The CLI can initialize a configuration file with placeholder credentials:
```bash
python -m alpaca_bot.cli init config.yaml
```
This will create `config.yaml` containing fields for `api_key`, `api_secret`, and
`base_url` written using safe YAML serialization.
