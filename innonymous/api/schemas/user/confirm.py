from pydantic import BaseModel


class UserConfirmSchema(BaseModel):
    captcha: str
    create_token: str
