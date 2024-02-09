from typing import Any
from uuid import UUID
from pydantic import BaseModel


class TaskBaseSchema(BaseModel):
    id: UUID = None
    status: str = None
    result: Any = None
    