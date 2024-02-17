from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Response

from database import SessionDepend

from .repos import User, UserRepository
from .schemas import UserOutSchema, UserInSchema, UserQuerySchema
from .security import Auth

router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/user/create',
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


@router.get('/user/{id}',
            name='Получить пользователя',
            tags=['get'],
            response_model=UserOutSchema | None
            )
async def user_get(
                    user_schema: Annotated[UserQuerySchema, Depends()],
                    session: Annotated[AsyncSession, Depends(SessionDepend)]
                    ):
    user: User | None = await UserRepository(session).get(user_schema)
    return user


@router.get('/user',
            name='Получить своего пользователя',
            tags=['get'],
            response_model=UserOutSchema
            )
async def user_get_me(subject: Annotated[dict, Depends(Auth.subject)]):
    return subject


@router.post('/login',
             name='login'
             )
async def user_login(
                    user_schema: UserInSchema,
                    session: Annotated[AsyncSession, Depends(SessionDepend)],
                    response: Response
                    ):
    if await UserRepository(session).verify(user_schema):
        await Auth.login(response=response, subject=dict(name=user_schema.name))
        return {'status': 'success'}
    raise HTTPException(401, 'Bad data')


@router.post('/refresh',
             name='Обновить Access JWT'
             )
async def user_refresh(
                        is_refreshed: Annotated[bool, Depends(Auth.refresh_access)]
                        ):
    if not is_refreshed:
        return HTTPException(403, 'Invalid refresh token')
    return {'status': 'success'}
