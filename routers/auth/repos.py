from hashlib import sha256

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Delete, Insert, Result, Select, Sequence, Update, delete, select, update

from database.model import User

from routers.auth.schemas import UserInSchema, UserQuerySchema

from database._abcrepos import Repository


class UserRepository(Repository):
    model: User = User
    session: AsyncSession

    async def create(self,
                     user_schema: UserInSchema
                     ) -> User:
        async with self.session as session:
            bytes_password: bytes = bytes(user_schema.password.get_secret_value(), encoding='utf-8')
            hashed_password: str = sha256(bytes_password).hexdigest()
            user: User = User(
                name=user_schema.name,
                hashed_password=hashed_password
            )
            session.add(user)
            await session.commit()
        return user
    
    async def update():
        ...

    async def get(self,
                  user_schema: UserQuerySchema
                  ) -> User | None:
        async with self.session as session:
            user: User | None = await session.get(User, user_schema.name)
        return user

    async def delete():
        ...

    async def verify(
            self,
            user_schema: UserInSchema
                    ) -> bool:
        async with self.session as session:
            user: User | None = await session.get(User, user_schema.name)
            if user and await self._verify_password(user_schema.password.get_secret_value(), user.hashed_password):
                return True
        return False

    @staticmethod
    async def _verify_password(password: str, hash: str) -> bool:
        return sha256(bytes(password, encoding='utf-8')).hexdigest() == hash
    