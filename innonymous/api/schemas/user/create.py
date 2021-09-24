from pydantic import (
    BaseModel,
    constr
)


class UserCreateSchema(BaseModel):
    name: constr(regex=r'^.{2,32}$')
