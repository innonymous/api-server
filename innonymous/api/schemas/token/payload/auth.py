from uuid import UUID

from pydantic import (
    BaseModel,
    Extra
)


class TokenAuthPayloadSchema(BaseModel):
    uuid: UUID

    class Config:
        extra = Extra.forbid
