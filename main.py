import uvicorn
from fastapi import FastAPI


async def lifespan(app: FastAPI) -> None:
    print('Start')
    yield
    print('End')


app: FastAPI = FastAPI(lifespan=lifespan)


if __name__ == '__main__':
    uvicorn.run('main:app', port=80, host='0.0.0.0', reload=True)
