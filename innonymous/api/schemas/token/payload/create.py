from pydantic import Extra

from innonymous.api.schemas.user import UserCreateSchema


class TokenCreatePayloadSchema(UserCreateSchema):
    captcha: str

    class Config:
        extra = Extra.forbid
