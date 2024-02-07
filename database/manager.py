from config import Settings

from alchemynger import AsyncManager


manager: AsyncManager = AsyncManager(path=Settings.DB_DSN)
