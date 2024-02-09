from sqlalchemy import Delete, Insert, Result, Select, Sequence, Update, delete, insert, select, update

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
    
    @classmethod
    async def get(cls,
                  author: AuthorUpdateSchema,
                  many: bool = True
                  ) -> Author | Sequence[Author] | None:
        async with manager.get_session() as session:
            stmt: Select = select(Author).filter_by(**author.model_dump(exclude_none=True))
            result: Result = await session.execute(stmt)
            if many:
                return result.scalars().all()
            return result.scalar_one_or_none()
    
    @classmethod
    async def delete(cls,
                     id: int
                     ) -> int | None:
        async with manager.get_session() as session:
            stmt: Delete = delete(Author).where(Author.id == id).returning(Author.id)
            result: Result = await session.execute(stmt)
            await session.commit()
            rid: int | None = result.scalar_one_or_none()
            return rid
