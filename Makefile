.PHONY: help setup run test lint clean

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "Available targets:"
	@echo "  setup     - Create virtual environment and install dependencies"
	@echo "  run       - Run the trading bot"
	@echo "  test      - Run tests"
	@echo "  lint      - Run ruff linter"
	@echo "  clean     - Remove virtual environment"

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev,web]

setup: $(VENV)/bin/activate

run: $(VENV)/bin/activate
	$(VENV)/bin/alpaca-bot run --mode paper

test: $(VENV)/bin/activate
	$(VENV)/bin/pytest

lint: $(VENV)/bin/activate
	$(VENV)/bin/ruff check .

clean:
	rm -rf $(VENV)
