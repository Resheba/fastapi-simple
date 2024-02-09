from tasks import celeryApp
from enum import Enum


class TaskType(str, Enum):
    summa = 'summa'
    sub = 'sub'


class ArithmTaskManager:
    @staticmethod
    @celeryApp.task
    def summa(a: int, b: int) -> int:
        return a + b
    
    @staticmethod
    @celeryApp.task
    def sub(a: int, b: int) -> int:
        return a - b
