from pydantic import (
    BaseModel,
    constr
)


class RoomCreateSchema(BaseModel):
    name: constr(regex=r'^[A-Za-z0-9 -_]{5,32}$')
