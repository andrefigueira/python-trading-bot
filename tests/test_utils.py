from alpaca_bot.core.utils import get_logger, retry


def test_get_logger_singleton():
    logger1 = get_logger('x')
    logger2 = get_logger('x')
    assert logger1 is logger2


def test_retry_success_after_failure():
    calls = {'n': 0}

    @retry(times=2, delay=0)
    def func():
        calls['n'] += 1
        if calls['n'] < 2:
            raise ValueError('fail')
        return 'ok'

    assert func() == 'ok'
    assert calls['n'] == 2
