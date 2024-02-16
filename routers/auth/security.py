from config import Settings

from datetime import timedelta
from fastapi import Response, Security
from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearerCookie, JwtAuthorizationCredentials


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
    @staticmethod
    def login():
        ...
        