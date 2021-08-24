"""
The entrypoint of the api. In this file will initialize all objects, that
the api uses, i.e. database, etc.
"""

from fastapi import FastAPI

api = FastAPI(
    version='0.0.1',
    title='InnonymousApi'
)
