from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    name: str
