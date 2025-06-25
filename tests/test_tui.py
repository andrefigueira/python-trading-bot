from alpaca_bot import tui


def test_tui_quit(capsys):
    inputs = iter(["5"])
    tui.run(lambda _: next(inputs))
    out = capsys.readouterr().out
    assert "alpaca-bot menu" in out
