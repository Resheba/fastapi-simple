from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Delete, Insert, Result, Select, Sequence, Update, delete, insert, select, update

from database.model import Author

from routers.author.schemas import AuthorInSchema, AuthorUpdateSchema
from ._abcrepos import Repository


class AuthorRepository(Repository):
    model: Author = Author
    session: AsyncSession

    async def create(self,
                     author: AuthorInSchema
                     ) -> int:
        async with self.session as session:
            stmt: Insert = insert(self.model).values(**author.model_dump()).returning(self.model.id)
            result: Result = await session.execute(stmt)
            author_id: int = result.scalar_one_or_none()
            await session.commit()
        return author_id
    
    async def update(self,
                     author: AuthorUpdateSchema
                     ) -> Author:
        async with self.session as session:
            stmt: Update = update(self.model).where(self.model.id == author.id).values(**AuthorInSchema.model_validate(author).model_dump(exclude_none=True))
            await session.execute(stmt)
            await session.commit()
            res_author: Author = (await session.execute(
                select(self.model).where(self.model.id == author.id)
                )).scalar_one()
        return res_author
    
    async def get(self,
                  author: AuthorUpdateSchema,
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
