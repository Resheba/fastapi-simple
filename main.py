import uvicorn
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import from_url

from database import manager
from config import Settings
from core import BaseHTTPException, base_exception_handler

from routers import AuthorRouter, ArithmRouter, UserRouter, AuthRouter


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    FastAPICache.init(
        RedisBackend(from_url(Settings.REDIS_DSN)),
        prefix='fcached'
        )
    
    app.include_router(AuthorRouter); app.include_router(ArithmRouter); app.include_router(UserRouter); app.include_router(AuthRouter)
    await manager.connect(create_all=False, expire_on_commit=False)
    print('Start')
    yield
    print('End')


app: FastAPI = FastAPI(
                       title='Simple Project',
                       lifespan=lifespan,
                       debug=True,
                       exception_handlers={
                           BaseHTTPException: base_exception_handler
                       }
                       )


if __name__ == '__main__':
    uvicorn.run('main:app', port=80, host='0.0.0.0', reload=True)
