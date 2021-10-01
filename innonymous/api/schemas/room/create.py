from pydantic import (
    BaseModel,
    constr
)


class RoomCreateSchema(BaseModel):
    name: constr(regex=r'^[A-Za-z0-9][A-Za-z0-9 \-_]{3,30}[A-Za-z0-9]$')
