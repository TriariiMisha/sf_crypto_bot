from abc import ABC, abstractmethod


class TaskManager(ABC):
    @abstractmethod
    def map(self, fun, array, *args, **kwargs):
        pass


class SimpleTaskManager(TaskManager):
    def map(self, fun, array, *args, **kwargs):
        results = [fun(item, *args, **kwargs) for item in array]

        return results
