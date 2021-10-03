from pydantic import (
    BaseModel,
    constr
)


class RoomCreateSchema(BaseModel):
    name: constr(regex=r'^[\w0-9][\w0-9\s\-_]{3,30}[\w0-9]$')
