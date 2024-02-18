from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path
from fastapi_cache.decorator import cache

from database import SessionDepend
from auth import Auth

from .repos import User, UserRepository
from .schemas import UserOutSchema, UserInSchema, UserQuerySchema

router: APIRouter = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/create',
             name='Создание пользователя',
             tags=['create'],
             response_model=UserOutSchema
             )
async def user_create(
                      user: UserInSchema, 
                      session: Annotated[AsyncSession, Depends(SessionDepend)]
                      ):
    user_out: User = await UserRepository(session).create(user)
    return user_out


@router.get('/{name}',
            name='Получить пользователя',
            tags=['get'],
            response_model=UserOutSchema | None
            )
# @cache(expire=10)
async def user_get(
                    username: Annotated[str, Path(alias='name', validation_alias='name')],
                    session: Annotated[AsyncSession, Depends(SessionDepend)]
                    ):
    user_schema: UserQuerySchema = UserQuerySchema(name=username)
    user: User | None = await UserRepository(session).get(user_schema)
    return user


@router.get('',
            name='Получить своего пользователя',
            tags=['get'],
            response_model=UserOutSchema
            )
async def user_get_me(subject: Annotated[dict, Depends(Auth.subject)]):
    return subject
