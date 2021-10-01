from uuid import UUID

from pydantic import Extra

from innonymous.api.schemas.user import UserCreateSchema


class TokenCreatePayloadSchema(UserCreateSchema):
    uuid: UUID
    captcha: str
    exp: float

    class Config:
        extra = Extra.forbid
