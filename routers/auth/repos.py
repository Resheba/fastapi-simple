from hashlib import sha256

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Delete, Insert, Result, Select, Sequence, Update, delete, select, update

from database.model import User

from routers.auth.schemas import UserInSchema

from database._abcrepos import Repository


class UserRepository(Repository):
    model: User = User
    session: AsyncSession

    async def create(self,
                     user_schema: UserInSchema
                     ) -> User:
        async with self.session as session:
            hashed_password: str = sha256(bytes(user_schema.password)).hexdigest()
            user: User = User(
                name=user_schema.name,
                hashed_password=hashed_password
            )
            session.add(user)
            await session.commit()
        return user
    