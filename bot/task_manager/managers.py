import asyncio

from abc import ABC, abstractmethod
from threading import Thread


class TaskManager(ABC):
    @abstractmethod
    def map(self, fun, array, *args, **kwargs):
        pass


class SimpleTaskManager(TaskManager):
    def map(self, fun, array, *args, **kwargs):
        results = [fun(item, *args, **kwargs) for item in array]

        return results


class ThreadTaskManager(TaskManager):
    def map(self, fun, array, *args, **kwargs):
        threads = []
        results = []

        for item in array:
            thread = Thread(target=lambda: results.append(fun(item, *args, **kwargs)))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return results


class AsyncTaskManager(TaskManager):
    async def map(self, fun, array, *args, **kwargs):
        tasks = [fun(item, *args, **kwargs) for item in array]
        results = await asyncio.gather(*tasks)

        return results
