from pydantic import BaseModel

from innonymous.database.models import MessageType


class MessageCreateSchema(BaseModel):
    type: MessageType
    data: bytes
