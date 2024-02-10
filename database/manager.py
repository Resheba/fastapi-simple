from config import Settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from alchemynger import AsyncManager


manager: AsyncManager = AsyncManager(path=Settings.DB_DSN)


async def SessionDepend() -> AsyncGenerator[AsyncSession, None]:
    async with manager.get_session() as session:
        yield session
