import asyncio
import logging
import threading
from abc import ABC, abstractmethod


class TaskManager(ABC):
    def __init__(self):
        logging.info(f'[TASK MANAGER] {__name__} initialized')

    @abstractmethod
    def map(self, fun, array, *args, **kwargs):
        pass


class SimpleTaskManager(TaskManager):
    def map(self, fun, array, *args, **kwargs):
        results = [fun(item, *args, **kwargs) for item in array]

        return results


class AsyncTaskManager(TaskManager):
    async def map(self, fun, array, *args, **kwargs):
        tasks = [fun(item, *args, **kwargs) for item in array]
        results = await asyncio.gather(*tasks)

        return results


class ThreadTaskManager(TaskManager):
    def map(self, fun, array, *args, **kwargs):
        results = []
        threads = []

        for item in array:
            thread = threading.Thread(target=lambda: results.append(fun(item, *args, **kwargs)))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results


class ProcessTaskManager(TaskManager):
    def map(self, fun, array, *args, **kwargs):
        results = ...

        return results
