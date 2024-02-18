from typing import Sequence
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase


class SerializatorDTO:
    @staticmethod
    def fromORM(
        _from: Sequence[DeclarativeBase] | DeclarativeBase,
        _to: BaseModel,
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
