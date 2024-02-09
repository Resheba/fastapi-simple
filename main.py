from typing import AsyncGenerator
import uvicorn
from fastapi import FastAPI

from database import manager

from routers import AuthorRouter


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print('Start')
    app.include_router(AuthorRouter)
    await manager.connect()
    yield
    print('End')


app: FastAPI = FastAPI(
                       lifespan=lifespan
                       )


if __name__ == '__main__':
    uvicorn.run('main:app', port=80, host='0.0.0.0', reload=True)
