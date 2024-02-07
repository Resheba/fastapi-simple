from typing import Annotated

from fastapi import HTTPException, Query


class TokenValidator:
    def __init__(self, token: Annotated[str, Query()] = '') -> None:
        if not token:
            raise HTTPException(status_code=400, detail='Token missed')
        