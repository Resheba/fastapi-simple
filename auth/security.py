from typing import Annotated

from pydantic import BaseModel

from config import Settings
from core import BaseHTTPException

from datetime import timedelta
from fastapi import Response, Security, status
from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearerCookie, JwtAuthorizationCredentials

from .schemas import SubjectSchema


class JWTSecurity:
    jwt_access: JwtAccessBearerCookie = JwtAccessBearerCookie(
        secret_key=Settings.JWT_SECRET,
        access_expires_delta=timedelta(minutes=1),
        refresh_expires_delta=timedelta(hours=1),
        auto_error=False
    )
    jwt_refresh: JwtRefreshBearerCookie = JwtRefreshBearerCookie.from_other(
        other=jwt_access
    )

    @classmethod
    def set_access_refresh(
        cls,
        response: Response, 
        subject: dict
    ) -> None:
        access_token: str = cls.jwt_access.create_access_token(subject=subject)
        refresh_token: str = cls.jwt_refresh.create_refresh_token(subject=subject)
        cls.jwt_access.set_access_cookie(response, access_token); cls.jwt_refresh.set_refresh_cookie(response, refresh_token)

    @classmethod
    def refresh(
        cls,
        response: Response,
        credentials: JwtAuthorizationCredentials
    ) -> None:
        access_token: str = cls.jwt_access.create_access_token(subject=credentials.subject)
        refresh_token: str = cls.jwt_refresh.create_refresh_token(subject=credentials.subject)
        cls.jwt_access.set_access_cookie(response, access_token); cls.jwt_refresh.set_refresh_cookie(response, refresh_token)
    

class Auth:
    @classmethod
    async def login(
                    cls,
                    response: Response,
                    subject: SubjectSchema | dict,
        ) -> None:
         if issubclass(BaseModel, type(subject)):
             subject: dict = subject.model_dump()
         JWTSecurity.set_access_refresh(response=response, subject=subject)
    
    @staticmethod
    async def subject(
                    credentials: Annotated[JwtAuthorizationCredentials, Security(JWTSecurity.jwt_access)]
        ) -> dict:
        if credentials:
            return credentials.subject
        raise BaseHTTPException(status.HTTP_401_UNAUTHORIZED, msg='Login required')
    
    @staticmethod
    async def refresh_access(
                            credentials: Annotated[JwtAuthorizationCredentials, Security(JWTSecurity.jwt_refresh)], 
                            response: Response
                            ) -> bool:
        if not credentials:
            return False
        JWTSecurity.refresh(response=response, credentials=credentials)
        return True
        