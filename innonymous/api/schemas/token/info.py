from pydantic import BaseModel


class TokenInfoSchema(BaseModel):
    access_token: str
