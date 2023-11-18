import contextlib

from fastapi import FastAPI
from routers import *

app = FastAPI(title='Boardlooker Backend API', version='0.0.1', docs_url='/swagger')

app.include_router(boardgames_router)
app.include_router(locations_router)
app.include_router(users_router)


@app.on_event('startup')
async def init_db():
    from database.models import Base
    from database.session import engine

    with contextlib.suppress(BaseException):
        Base.metadata.create_all(engine)
