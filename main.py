import uvicorn
from fastapi import FastAPI

from database import manager
from database.model import Author, Post


async def lifespan(app: FastAPI) -> None:
    print('Start')
    await manager.connect()
    yield
    print('End')


app: FastAPI = FastAPI(lifespan=lifespan)


@app.get('/')
async def test():
    # await manager.execute(manager[Author].insert.values(name='Lex'), commit=True)
    async with manager.get_session() as session:
        # await session.execute(manager[Post].insert.values(title='NewState', author_id=1))
        # await session.commit()
        author: Author = (await session.execute(manager[Author].select)).scalar_one()
        print(author.posts)


if __name__ == '__main__':
    uvicorn.run('main:app', port=80, host='0.0.0.0', reload=True)
