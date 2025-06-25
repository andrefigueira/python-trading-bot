from __future__ import annotations

from typing import Callable

from . import cli


def run(input_func: Callable[[str], str] = input) -> None:
    """Simple text-based UI to control the bot."""
    while True:
        print("\n*** alpaca-bot menu ***")
        print("1. Start bot")
        print("2. Show portfolio")
        print("3. Show orders")
        print("4. Set symbols")
        print("5. Quit")
        choice = input_func("Select option: ").strip()
        if choice == "1":
            cli.run(no_ui=True)
        elif choice == "2":
            cli.portfolio()
        elif choice == "3":
            cli.orders()
        elif choice == "4":
            symbols = input_func("Symbols (comma-separated): ")
            cli.set_symbols(symbols)
        elif choice == "5":
            break
        else:
            print("Invalid choice")
