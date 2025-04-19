import logging
import os
from datetime import datetime
from time import sleep

from bot.args_parser.args import Duration
from bot.args_parser.parser import parser
from bot.consts import RPS_LIMIT
from bot.data_handler.handlers import PickleDataHandler
from bot.requester.requesters import HTTPAsyncRequester, HTTPRequester
from bot.task_manager.managers import (AsyncTaskManager, SimpleTaskManager,
                                       ThreadTaskManager)
from bot.utils import get_time_to_sleep, get_timestamp

logging.basicConfig(
    level=logging.INFO, filename='py_log.log', filemode='a', format='%(asctime)s %(levelname)s %(message)s'
)


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

        logging.info('[COLLECTOR] process successfully initialized with parameters:')

        logging.info(f'\t tickers: {", ".join(self.tickers)}')
        logging.info(f'\t duration: {self.seconds} seconds')

    async def run(self):
        # get requester
        # requester = HTTPAsyncRequester(headers=dict())
        requester = HTTPRequester(headers=dict())

        # get data handler
        data_handler = PickleDataHandler()

        # get runs mapper
        # task_manager = AsyncTaskManager()
        # task_manager = SimpleTaskManager()
        task_manager = ThreadTaskManager()

        # run
        ts_current = get_timestamp(datetime.now())
        ts_to_finish = ts_current + self.seconds

        seconds_to_sleep, real_rps = get_time_to_sleep(RPS_LIMIT, len(self.tickers))

        logging.info(
            f'[COLLECTOR] due to rps limit {RPS_LIMIT} sleep interval is {seconds_to_sleep:.2f} (real rps is {real_rps})'
        )

        while ts_to_finish > ts_current:
            sync_ts = get_timestamp(datetime.now(), units='ns')

            # results = await task_manager.map(requester.get, self.tickers, sync_ts=sync_ts)
            results = task_manager.map(requester.get, self.tickers, sync_ts=sync_ts)

            data_handler.write(results)

            sleep(seconds_to_sleep)

            ts_current = get_timestamp(datetime.now())

        # close all connections
        # await requester.close()
        requester.close()
