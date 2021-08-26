"""
The entrypoint of the api. In this file will initialize all objects, that
the api uses, i.e. database, etc.
"""

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from innonymous.api.settings import APISettings
from innonymous.api.utils import Captcha
from innonymous.api.utils.auth import JWTAuthenticator
from innonymous.database import DatabaseEngine

settings = APISettings()

app = FastAPI(
    version='0.0.1',
    title='InnonymousApi'
)

db_engine = DatabaseEngine(
    settings.database_url
)

auth = JWTAuthenticator(
    settings.key,
    db_engine.session
)

captcha = Captcha(
    settings.key,
    settings.captcha_store
)

from innonymous.api.views import users, rooms, messages

app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(messages.router)

app.mount(
    '/captcha',
    StaticFiles(
        directory=settings.captcha_store
    )
)
