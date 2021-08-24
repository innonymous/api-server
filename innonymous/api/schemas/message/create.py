from pydantic import BaseModel


class MessageCreateSchema(BaseModel):
    type: str
    data: bytes
