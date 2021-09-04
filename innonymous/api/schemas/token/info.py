from uuid import UUID

from pydantic import BaseModel


class TokenInfoSchema(BaseModel):
    uuid: UUID
    access_token: str
