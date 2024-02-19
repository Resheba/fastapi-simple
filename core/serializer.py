import asyncio
from functools import wraps
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from typing import Any, Callable, Sequence, Type


class SerializatorDTO:
    def __init__(self, _to: Type[BaseModel]) -> None:
        self._to = _to

    @staticmethod
    def fromORM(
        _from: Sequence[DeclarativeBase] | DeclarativeBase,
        _to: Type[BaseModel],
        /
        ) -> Sequence[BaseModel] | BaseModel:
        if _from is None:
            return _from
        if issubclass(type(_from), Sequence):
            return tuple(
                _to.model_validate(fr, from_attributes=True)
                for fr in _from
            )
        return _to.model_validate(_from, from_attributes=True)

    def __call__(self, func: Callable) -> Any:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> self._to:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            return self.fromORM(result, self._to)
        return wrapper
