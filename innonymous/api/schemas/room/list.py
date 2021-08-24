from pydantic import BaseModel

from innonymous.api.schemas.room.info import RoomInfoSchema


class RoomListSchema(BaseModel):
    rooms: list[RoomInfoSchema]
