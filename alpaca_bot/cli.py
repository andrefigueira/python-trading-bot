import click
import yaml

@click.group()
def cli():
    """Alpaca trading bot command line interface."""
    pass

@cli.command()
@click.argument('path', type=click.Path(dir_okay=False))
def init(path):
    """Create a default configuration file in YAML format."""
    config = {
        'alpaca': {
            'key_id': 'YOUR_KEY_ID',
            'secret_key': 'YOUR_SECRET_KEY'
        }
    }
    with open(path, 'w') as f:
        yaml.safe_dump(config, f)
    click.echo(f"Configuration written to {path}")

if __name__ == '__main__':
    cli()
