from pydantic import (
    BaseModel,
    constr
)


class UserCreateSchema(BaseModel):
    name: constr(regex=r'^[A-Za-z0-9А-Яа-яЁё][A-Za-z0-9А-Яа-яЁё \-_]{0,30}[A-Za-z0-9А-Яа-яЁё]$')
