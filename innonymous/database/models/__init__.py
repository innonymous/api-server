from sqlalchemy.orm import declarative_base

Base = declarative_base()

from innonymous.database.models.user import User
from innonymous.database.models.room import Room
from innonymous.database.models.message import MessageType, Message
