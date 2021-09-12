from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, validator

from innonymous.database.models import MessageType


class MessageInfoSchema(BaseModel):
    uuid: UUID
    user_uuid: UUID
    room_uuid: UUID
    time: datetime
    type: MessageType
    data: bytes = None

    @validator('time')
    def convert_time(cls, time: datetime) -> datetime:
        return time.replace(tzinfo=timezone.utc)

    class Config:
        orm_mode = True
