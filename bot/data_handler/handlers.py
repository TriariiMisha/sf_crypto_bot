import logging
import os
import pickle
from abc import ABC, abstractmethod
from datetime import datetime

from bot.utils import get_timestamp


class DataHandler(ABC):
    def __init__(self, folder='temp'):
        # process folder
        if not os.path.exists(folder):
            os.mkdir(folder)

        self.folder = folder

    @abstractmethod
    def write(self, items):
        pass


class PickleDataHandler(DataHandler):
    def write(self, items):
        timestamp = get_timestamp(datetime.now(), units='ns')
        filepath = f'{self.folder}/{timestamp}.pickle'

        with open(filepath, 'wb') as file:
            pickle.dump(items, file)

        logging.info(f'[DATA HANDLER] items are saved to file {filepath}...')


class CsvDataHandler(DataHandler):
    def write(self, items):
        pass
