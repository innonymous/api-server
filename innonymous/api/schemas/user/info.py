from uuid import UUID

from pydantic import BaseModel


class UserInfoSchema(BaseModel):
    uuid: UUID
    name: str

    class Config:
        orm_mode = True
