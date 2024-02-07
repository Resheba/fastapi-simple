from abc import ABC, abstractmethod
from sqlalchemy.orm import DeclarativeBase


class Repository(ABC):
    model: DeclarativeBase

    @abstractmethod
    def create():
        ...

    @abstractmethod
    def update():
        ...

    @abstractmethod
    def delete():
        ...

    @abstractmethod
    def get():
        ...
