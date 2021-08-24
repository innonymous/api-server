"""
The entrypoint of the api. In this file will initialize all objects, that
the api uses, i.e. database, etc.
"""

from fastapi import FastAPI

from innonymous.api.settings import APISettings
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
    settings.jwt_key,
    db_engine.session
)

from innonymous.api.views import user, room, message

app.include_router(user.router)
app.include_router(room.router)
app.include_router(message.router)
