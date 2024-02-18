from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_cache.decorator import cache

from database import SessionDepend
from auth import Auth

from ..user.schemas import UserInSchema
from ..user.repos import UserRepository


router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('',
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


@router.put('',
             name='Обновить Access JWT'
             )
async def user_refresh(
                        is_refreshed: Annotated[bool, Depends(Auth.refresh_access)]
                        ):
    if not is_refreshed:
        return HTTPException(403, 'Invalid refresh token')
    return {'status': 'success'}
