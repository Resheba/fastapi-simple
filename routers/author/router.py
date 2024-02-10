from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionDepend
from database.model import Author
from database.repos import AuthorRepository

from .schemas import AuthorInSchema, AuthorUpdateSchema
from .depends import TokenValidator, AuthorUpdateQuery, TokenLazyValidator


router: APIRouter = APIRouter(
    prefix='/author',
    tags=['Author'],
    )


@router.post('/create',
             name='Создание Автора',
             tags=['create'],
             dependencies=[Depends(TokenValidator)]
             )
async def author_create(
                        author: AuthorInSchema,
                        session: Annotated[AsyncSession, Depends(SessionDepend)]
                        ) -> int:
    author_id: int = await AuthorRepository(session).create(author)
    return author_id


@router.put('/update',
            name='Изменение Автора',
            tags=['update'],
            response_model=AuthorInSchema,
            dependencies=[Depends(TokenValidator)]
            )
async def author_update(
                        author: AuthorUpdateSchema,
                        session: Annotated[AsyncSession, Depends(SessionDepend)]
                        ):
    author: Author = await AuthorRepository(session).update(author)
    return author


@router.get('/get',
            name='Получить Авторов',
            tags=['get'],
            response_model=list[AuthorInSchema | AuthorUpdateSchema]
            )
async def authors_get(
                      query: Annotated[AuthorUpdateQuery, Depends(AuthorUpdateQuery)], 
                      token: Annotated[TokenLazyValidator, Depends(TokenLazyValidator)],
                      session: Annotated[AsyncSession, Depends(SessionDepend)]
                      ):
    author: AuthorUpdateSchema = AuthorUpdateSchema(**query.params())
    authors: list[Author] = await AuthorRepository(session).get(author=author)
    if token.is_valid():
        return (AuthorUpdateSchema.model_validate(author, from_attributes=True) for author in authors)
    return authors


@router.get('/{id}',
            name='Получить Автора',
            tags=['get'],
            response_model=AuthorInSchema,
            responses={
                   404: {'description': 'No Author with {id=}'}
               }
            )
async def author_get(
                        id: Annotated[int, Path(ge=1, title='Идентификатор', description='Идентификатор автора')],
                        session: Annotated[AsyncSession, Depends(SessionDepend)]
                        ):
    author_schema: AuthorUpdateSchema = AuthorUpdateSchema(id=id)
    author: Author | None = await AuthorRepository(session).get(author=author_schema, many=False)
    if author:
        return author
    raise HTTPException(status_code=404, detail=f'No Author with {id=}')


@router.delete('/{id}',
               name='Удалить Автора',
               tags=['delete'],
               response_model=int,
               dependencies=[Depends(TokenValidator)],
               responses={
                   404: {'description': 'No Author with {id=}'},
                   400: {'description': 'Token missed'}
               }
               )
async def author_delete(
                        id: Annotated[int, Path(ge=1, title='Идентификатор', description='Идентификатор автора')],
                        session: Annotated[AsyncSession, Depends(SessionDepend)]
                        ):
    author_id: int | None = await AuthorRepository(session).delete(id=id)
    if author_id:
        return author_id
    raise HTTPException(status_code=404, detail=f'No Author with {id=}')
