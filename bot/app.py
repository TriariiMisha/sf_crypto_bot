import os
from datetime import datetime
from time import sleep

from bot.args_parser.args import Duration
from bot.args_parser.parser import parser
from bot.consts import RPS_LIMIT
from bot.utils import get_time_to_sleep, get_timestamp


class Collector:
    @staticmethod
    def _process_tickers(path: str) -> list:
        if not os.path.isfile(path):
            raise ValueError(f'{path} is not a file!')

        with open(path, 'r') as file:
            tickers = file.read().split(',')

        return tickers

    @classmethod
    def from_args(cls):
        args = parser.parse_args()

        args_dict = {
            'tickers_file': args.tickers,
            'duration_string': args.duration,
        }

        instance = cls(**args_dict)

        return instance

    def __init__(self, tickers_file: str, duration_string=''):
        # process tickers
        self.tickers = self._process_tickers(tickers_file)

        # process duration
        duration = Duration(duration_string)
        self.seconds = duration.to_seconds()

        print('[MVP] process successfully initialized with parameters:')

        print(f'\t tickers: {", ".join(self.tickers)}')
        print(f'\t duration: {self.seconds} seconds')

    def run(self):
        # run
        ts_current = get_timestamp(datetime.now())
        ts_to_finish = ts_current + self.seconds

        seconds_to_sleep, real_rps = get_time_to_sleep(RPS_LIMIT, len(self.tickers))

        print(
            f'[MVP] due to rps limit {RPS_LIMIT} sleep interval is {seconds_to_sleep:.2f} (real rps is {real_rps})'
        )