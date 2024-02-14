from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Delete, Insert, Result, Select, Sequence, Update, delete, select, update

from database.model import Author

from routers.author.schemas import AuthorInSchema, AuthorUpdateSchema, AuthorQuerySchema
from ._abcrepos import Repository


class AuthorRepository(Repository):
    model: Author = Author
    session: AsyncSession

    async def create(self,
                     author: AuthorInSchema
                     ) -> Author:
        async with self.session as session:
            author_orm: Author = Author(**author.model_dump())
            session.add(author_orm)
            await session.commit()
        return author_orm
    
    async def update(self,
                     author: AuthorUpdateSchema
                     ) -> Author | None:
        async with self.session as session:
            author_orm: Author = await session.get(Author, author.id)
            if author_orm:
                [setattr(author_orm, attr, value) for attr, value in author.model_dump(exclude_none=True).items()]
                # author_orm.__dict__.update(author.model_dump(exclude_none=True))
                await session.commit()
                return author_orm
    
    async def get(self,
                  author: AuthorQuerySchema,
                  many: bool = True
                  ) -> Author | Sequence[Author] | None:
        async with self.session as session:
            stmt: Select = select(self.model).filter_by(**author.model_dump(exclude_none=True))
            result: Result = await session.execute(stmt)
            if many:
                return result.scalars().all()
            return result.scalar_one_or_none()
    
    async def delete(self,
                     id: int
                     ) -> int | None:
        async with self.session as session:
            stmt: Delete = delete(self.model).where(self.model.id == id).returning(self.model.id)
            result: Result = await session.execute(stmt)
            await session.commit()
            rid: int | None = result.scalar_one_or_none()
            return rid
