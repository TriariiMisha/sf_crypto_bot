import logging
from abc import ABC, abstractmethod

import aiohttp
from requests import Session

from bot.consts import REST_URL as URL


class Requester(ABC):
    @abstractmethod
    def get(self, ticker, sync_ts):
        pass


class HTTPRequester(Requester):
    @staticmethod
    def _validate_response(response):
        try:
            response_data = response.json()
        except Exception as e:
            logging.error(
                f'[REQUESTER] an exception occured during response validation: {str(e)}'
            )
            return dict()

        if (message := response_data.get('retMsg')) == 'OK':
            return response_data
        else:
            logging.warn(
                f'[REQUESTER] not ok response catched during response validation: {message}'
            )
            return dict()

    @staticmethod
    def _process_response(data, ticker, sync_ts) -> dict:
        result = data.get('result', {})

        symbol = result.get('s', ticker)
        best_bid_price, best_bid_volume = result.get('b', [[None, None]])[0]
        best_ask_price, best_ask_volume = result.get('a', [[None, None]])[0]
        timestamp = result.get('ts')

        handled = {
            'sync_ts': sync_ts,
            'symbol': symbol,
            'timestamp': timestamp,
            'best_bid_price': best_bid_price,
            'best_bid_volume': best_bid_volume,
            'best_ask_price': best_ask_price,
            'best_ask_volume': best_ask_volume,
        }

        return handled

    def close(self):
        self.session.close()

        logging.info('[CONNECTOR] session closed!')

    def __init__(self, headers):
        session = Session()
        session.headers.update(headers)

        self.session = session

        logging.info('[CONNECTOR] new session established...')

    def get(self, ticker, sync_ts: int) -> dict:
        url = f'{URL}&symbol={ticker}'

        response = self.session.get(url)
        response_data = self._validate_response(response)
        response_processed = self._process_response(response_data, ticker, sync_ts)

        return response_processed


class HTTPAsyncRequester(HTTPRequester):
    @staticmethod
    async def _validate_response(response):
        try:
            response_data = await response.json()
        except Exception as e:
            logging.error(
                f'[REQUESTER] an exception occured during response validation: {str(e)}'
            )
            return dict()

        if (message := response_data.get('retMsg')) == 'OK':
            return response_data
        else:
            logging.warn(
                f'[REQUESTER] not ok response catched during response validation: {message}'
            )
            return dict()

    async def close(self):
        await self.session.close()

        logging.info('[CONNECTOR] session closed!')

    def __init__(self, headers):
        session = aiohttp.ClientSession()
        session.headers.update(headers)

        self.session = session

        logging.info('[CONNECTOR] new session established...')

    async def get(self, ticker, sync_ts: int) -> dict:
        url = f'{URL}&symbol={ticker}'

        response = await self.session.get(url)
        response_data = await self._validate_response(response)
        response_processed = self._process_response(response_data, ticker, sync_ts)

        return response_processed
