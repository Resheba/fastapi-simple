from typing import Annotated

from fastapi import HTTPException, Query
from pydantic import EmailStr


class TokenValidator:
    def __init__(self, token: Annotated[str, Query()] = '') -> None:
        if not token:
            raise HTTPException(status_code=400, detail='Token missed')
        

class TokenLazyValidator:
    def __init__(self, token: Annotated[str, Query()] = '') -> None:
        self.token: str = token
    
    def validate(self) -> None:
        if not self.token:
            raise HTTPException(status_code=400, detail='Token missed')
    
    def is_valid(self) -> bool:
        return bool(self.token)
        

class AuthorUpdateQuery:
    def __init__(self, 
                name: Annotated[str, Query(max_length=40, title='Имя', description='Имя автора')] = None, 
                age: Annotated[int, Query(ge=18, le=150, title='Возраст', description='Возраст автора')] = None,
                email: Annotated[EmailStr, Query(max_length=50, title='Почта', description='Почта автора')] = None
                ) -> None:
        self.name: str = name; self.age: int = age; self.email: EmailStr = email
