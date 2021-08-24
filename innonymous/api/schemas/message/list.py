from pydantic import BaseModel

from innonymous.api.schemas.message.info import MessageInfoSchema


class MessageListSchema(BaseModel):
    messages: list[MessageInfoSchema]
