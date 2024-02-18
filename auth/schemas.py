from pydantic import BaseModel


class SubjectSchema(BaseModel):
    name: str
