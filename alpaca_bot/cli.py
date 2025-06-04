import argparse
import yaml

def init(config_path: str) -> None:
    """Create a default configuration YAML file."""
    sample_config = {
        "api_key": "YOUR_API_KEY",
        "api_secret": "YOUR_API_SECRET",
        "base_url": "https://paper-api.alpaca.markets",
    }
    with open(config_path, "w") as f:
        yaml.safe_dump(sample_config, f)

def main(argv=None):
    parser = argparse.ArgumentParser(description="Alpaca trading bot CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="initialize configuration")
    init_parser.add_argument("config", help="path to config yaml")

    args = parser.parse_args(argv)
    if args.command == "init":
        init(args.config)

if __name__ == "__main__":
    main()
