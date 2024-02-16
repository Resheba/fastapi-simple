from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

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
    print(subject)
    return subject


@router.post('/login',
             name='Получить JWT Cookie',
             dependencies=[Depends(Auth.login)]
             )
async def user_login():
    return {'status': 200}


@router.post('/refresh',
             name='Обновить Access JWT',
             dependencies=[Depends(Auth.refresh_access)]
             )
async def user_refresh():
    return {'status': 200}
