from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


class AuthorInSchema(BaseModel):
    name: str
    age: int
    email: Optional[EmailStr] = None

    @validator('age')
    def age_validator(cls, age: int) -> int:
        if age < 18:
            raise ValueError('Author is\'t adult')
        return age
    

class AuthorUpdateSchema(AuthorInSchema):
    id: int = Field(ge=1)
    name: str | None = None
    age: int | None = None


class AuthorQuerySchema(AuthorUpdateSchema):
    id: int = Field(default=None)


class Post(BaseModel):
    id: int
    title: str
    author_id: int
    text: Optional[str] = None


class AuthorDTO(BaseModel):
    id: int
    name: str
    age: int
    email: Optional[EmailStr] = None
    # posts: list[Post] = Field(default_factory=list)
    