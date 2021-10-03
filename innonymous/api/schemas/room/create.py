from pydantic import (
    BaseModel,
    constr
)


class RoomCreateSchema(BaseModel):
    name: constr(regex=r'^[A-Za-z0-9А-Яа-яЁё][A-Za-z0-9А-Яа-яЁё \-_]{3,30}[A-Za-z0-9А-Яа-яЁё]$')
