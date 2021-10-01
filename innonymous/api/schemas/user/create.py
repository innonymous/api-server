from pydantic import (
    BaseModel,
    constr
)


class UserCreateSchema(BaseModel):
    name: constr(regex=r'^[A-Za-z0-9][A-Za-z0-9 \-_]{0,30}[A-Za-z0-9]$')
