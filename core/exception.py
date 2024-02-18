from typing import Any
from fastapi import Request
from fastapi.responses import JSONResponse

from .response import BaseResponse


class BaseHTTPException(Exception):
    def __init__(
            self, 
            status_code: int, 
            msg: str | None = None, 
            data: Any = None
            ) -> None:
        self.status_code = status_code; self.msg = msg; self.data = data


async def base_exception_handler(request: Request, ex: BaseHTTPException) -> JSONResponse:
    status: str = 'success'
    if 400 <= ex.status_code < 500:
        status: str = 'error'
    elif ex.status_code >= 500:
        status: str = 'fail'
    return JSONResponse(
        status_code=ex.status_code,
        content=BaseResponse(
            status=status,
            msg=ex.msg,
            data=ex.data
        ).model_dump(exclude_none=True)
    )
