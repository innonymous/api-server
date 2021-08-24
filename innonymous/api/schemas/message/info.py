from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from innonymous.database.models import MessageType


class MessageInfoSchema(BaseModel):
    uuid: UUID
    user_uuid: UUID
    room_uuid: UUID
    time: datetime
    type: MessageType
    data: bytes = None

    class Config:
        orm_mode = True
