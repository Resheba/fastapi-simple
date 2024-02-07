from fastapi import APIRouter, Depends

from database.model import Author

from .schemas import AuthorInSchema, AuthorUpdateSchema
from .depends import TokenValidator
from database.repos import AuthorRepository


router: APIRouter = APIRouter(
    prefix='/author',
    tags=['Author'],
    )


@router.post('/create',
             name='Создание Автора',
             tags=['create'],
             dependencies=[Depends(TokenValidator)]
             )
async def author_create(author: AuthorInSchema) -> int:
    author_id: int = await AuthorRepository.create(author)
    return author_id


@router.put('/update',
            name='Изменение Автора',
            tags=['update'],
            response_model=AuthorInSchema,
            dependencies=[Depends(TokenValidator)]
            )
async def author_update(author: AuthorUpdateSchema):
    author: Author = await AuthorRepository.update(author)
    return author
