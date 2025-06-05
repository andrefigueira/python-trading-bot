.PHONY: help setup run test lint clean

PYTHON_VERSION = 3.11
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
	pyenv install --skip-existing $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	python -m venv $(VENV)
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
