from sqlalchemy import Insert, Result, Select, Update, insert, select, update

from database import manager
from database.model import Author

from routers.author.schemas import AuthorInSchema, AuthorUpdateSchema
from ._abcrepos import Repository


class AuthorRepository(Repository):
    model = Author

    @classmethod
    async def create(cls,
                     author: AuthorInSchema
                     ) -> int:
        async with manager.get_session() as session:
            stmt: Insert = insert(Author).values(**author.model_dump()).returning(Author.id)
            result: Result = await session.execute(stmt)
            author_id: int = result.scalar_one_or_none()
            await session.commit()
        return author_id
    
    @classmethod
    async def update(cls,
                     author: AuthorUpdateSchema
                     ) -> Author:
        async with manager.get_session() as session:
            stmt: Update = update(Author).where(Author.id == author.id).values(**AuthorInSchema.model_validate(author).model_dump(exclude_none=True))
            await session.execute(stmt)
            await session.commit()
            res_author: Author = (await session.execute(
                select(Author).where(Author.id == author.id)
                )).scalar_one()
        return res_author
