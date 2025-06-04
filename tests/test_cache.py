from alpaca_bot.data.cache import DataCache


def test_data_cache():
    cache = DataCache()
    cache.add_bar('AAPL', '1D', {'c': 1})
    assert cache.last_bar('AAPL', '1D') == {'c': 1}
    cache.add_bar('AAPL', '1D', {'c': 2})
    assert cache.last_bar('AAPL', '1D') == {'c': 2}
