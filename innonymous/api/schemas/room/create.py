from pydantic import BaseModel


class RoomCreateSchema(BaseModel):
    name: str
