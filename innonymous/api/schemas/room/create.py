from pydantic import (
    BaseModel,
    constr
)


class RoomCreateSchema(BaseModel):
    name: constr(regex=r'^.{5,32}$')
