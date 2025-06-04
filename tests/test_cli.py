import os
import yaml
from click.testing import CliRunner
from alpaca_bot.cli import cli


def test_init_creates_valid_yaml(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    runner = CliRunner()
    result = runner.invoke(cli, ["init", str(cfg_file)])
    assert result.exit_code == 0
    assert cfg_file.exists()
    # Ensure the file contains valid YAML
    with open(cfg_file, 'r') as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict)
    assert 'alpaca' in data
