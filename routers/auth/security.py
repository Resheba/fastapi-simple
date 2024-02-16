from hashlib import sha256
from typing import Annotated

from config import Settings
from database import SessionDepend

from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, Security, Depends, HTTPException
from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearerCookie, JwtAuthorizationCredentials

from .repos import User, UserRepository
from .schemas import UserInSchema


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
                    user_schema: UserInSchema,
                    session: Annotated[AsyncSession, Depends(SessionDepend)]
        ) -> None:
        user: User | None = await UserRepository(session).get(user_schema)
        if not user:
            raise HTTPException(403, detail='No user')
        if await cls._verify_password(user_schema.password.get_secret_value(), user.hashed_password):
            JWTSecurity.set_access_refresh(response=response, subject=dict(name=user.name))
            return
        raise HTTPException(403, detail='Bad password')

    @staticmethod
    async def _verify_password(password: str, hash: str) -> bool:
        return sha256(bytes(password, encoding='utf-8')).hexdigest() == hash
    
    @staticmethod
    async def subject(
                    credentials: Annotated[JwtAuthorizationCredentials, Security(JWTSecurity.jwt_access)]
        ) -> dict:
        if credentials:
            return credentials.subject
        raise HTTPException(401, detail='Unauth')
    
    @staticmethod
    async def refresh_access(
                            credentials: Annotated[JwtAuthorizationCredentials, Security(JWTSecurity.jwt_refresh)], 
                            response: Response
                            ) -> None:
        JWTSecurity.refresh(response=response, credentials=credentials)
        