from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    LargeBinary
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from innonymous.database.models import Base
from innonymous.database.models.message.type import MessageType


class MessageModel(Base):
    __tablename__ = 'messages'

    uuid: UUID = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    time: datetime = Column(DateTime(), default=datetime.utcnow, nullable=False)
    type: MessageType = Column(Enum(MessageType), nullable=False)
    data: bytes = Column(LargeBinary(), nullable=True)

    user_uuid = Column(
        UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False
    )
    room_uuid = Column(
        UUID(as_uuid=True), ForeignKey('rooms.uuid'), nullable=False
    )

    user = relationship('UserModel', back_populates='messages')
    room = relationship('RoomModel', back_populates='messages')
