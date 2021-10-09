"""
The entrypoint of the api. In this file will initialize all objects, that
the api uses, i.e. database, etc.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from innonymous.api.settings import APISettings
from innonymous.api.utils import (
    Captcha,
    MessageQueue
)
from innonymous.api.utils.auth import JWTAuthenticator
from innonymous.database import DatabaseEngine

settings = APISettings()

app = FastAPI(
    version='1.0.1', title='InnonymousApi', root_path=settings.root_path or ''
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

captcha = Captcha(settings.key)
mq = MessageQueue(settings.amqp_url)
db_engine = DatabaseEngine(settings.database_url)
auth = JWTAuthenticator(settings.key, db_engine.session)


@app.on_event('startup')
async def on_startup() -> None:
    await mq.initialize()


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await mq.finalize()
    await db_engine.finalize()


# Import all views.
from innonymous.api.views import (
    users,
    rooms,
    messages
)

app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(messages.router)
