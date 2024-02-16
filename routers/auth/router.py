from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionDepend
from .repos import User, UserRepository

from .schemas import UserOutSchema, UserInSchema

router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth']
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
