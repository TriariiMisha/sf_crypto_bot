import re

RPS_LIMIT = 120
DURATION_PATTERN = re.compile('\d+\.*\d*[d|h|m|s]')
REST_URL = 'https://api.bybit.com/v5/market/orderbook?category=spot&limit=1'

TIME_CONFIG = {
    's': 10**0,
    'ms': 10**3,
    'ns': 10**6,
}
