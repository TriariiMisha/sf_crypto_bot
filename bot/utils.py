from datetime import datetime
from math import log

from bot.consts import TIME_CONFIG


def get_timestamp(dt: datetime, units='s') -> int:
    multiplier = TIME_CONFIG[units]
    timestamp = int(dt.timestamp() * multiplier)

    return timestamp


def get_time_to_sleep(limit_per_second, tickers_number) -> tuple:
    requests_per_second = limit_per_second / (
        tickers_number + (1 + log(tickers_number))
    )
    seconds_to_wait = 1 / requests_per_second
    real_requests_per_second = int(1 / seconds_to_wait * tickers_number)

    return seconds_to_wait, real_requests_per_second
