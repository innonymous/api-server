from pydantic import (
    BaseModel,
    constr
)


class RoomCreateSchema(BaseModel):
    name: constr(regex=r'^.{2,32}$')
