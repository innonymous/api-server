from sqlalchemy.orm import declarative_base

Base = declarative_base()

from innonymous.database.models.user import UserModel
from innonymous.database.models.room import RoomModel
from innonymous.database.models.message import (
    MessageType,
    MessageModel
)
from innonymous.database.models.i_time_trackable import ITimeTrackable
