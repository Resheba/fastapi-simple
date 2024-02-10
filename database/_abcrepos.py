from abc import ABC, abstractmethod
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class Repository(ABC):
    model: DeclarativeBase
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

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
