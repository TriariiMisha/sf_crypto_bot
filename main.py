import asyncio

from bot.app import Collector

if __name__ == '__main__':
    collector = Collector.from_args()
    asyncio.run(collector.run())
