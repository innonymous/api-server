from pydantic import (
    BaseModel,
    constr
)


class UserCreateSchema(BaseModel):
    name: constr(regex=r'^[\w0-9][\w0-9\s\-_]{0,30}[\w0-9]$')
