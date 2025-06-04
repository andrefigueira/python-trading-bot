import yaml
from alpaca_bot import cli


def test_init_writes_valid_yaml(tmp_path):
    config = tmp_path / "config.yaml"
    cli.init(str(config))
    with open(config) as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict)
    assert data["api_key"] == "YOUR_API_KEY"
