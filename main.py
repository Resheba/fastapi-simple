import uvicorn
from typing import AsyncGenerator
from fastapi import FastAPI

from database import manager

from routers import AuthorRouter, ArithmRouter, AuthRouter


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print('Start')
    app.include_router(AuthorRouter); app.include_router(ArithmRouter); app.include_router(AuthRouter)
    await manager.connect(create_all=False, expire_on_commit=False)
    yield
    print('End')


app: FastAPI = FastAPI(
                       lifespan=lifespan
                       )


if __name__ == '__main__':
    uvicorn.run('main:app', port=80, host='0.0.0.0', reload=True)
