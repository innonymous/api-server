from uuid import UUID

from pydantic import BaseModel


class TokenPayloadSchema(BaseModel):
    uuid: UUID
