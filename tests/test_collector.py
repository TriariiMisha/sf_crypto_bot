import unittest

from bot.app import Collector


class TestCollectorInit(unittest.TestCase):
    def setUp(self):
        """Метод выполняется перед каждым тестовым случаем."""
        self.tickers_file = 'data/tickers.txt'
        self.duration_string = '1s'

    def test_collector_init(self):
        collector = Collector(self.tickers_file, self.duration_string)

        assert hasattr(collector, 'tickers')
        assert hasattr(collector, 'seconds')

    def test_collector_init_incorrect_path(self):
        with self.assertRaises(ValueError):
            _ = Collector('data/trash.txt', self.duration_string)
