from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, LargeBinary, Enum
from sqlalchemy.dialects.postgresql import UUID

from innonymous.database.models import Base
from innonymous.database.models.message import MessageType


class Message(Base):
    __tablename__ = 'messages'

    uuid: UUID = Column(
        UUID(as_uuid=True),
        primary_key=True
    )
    time: datetime = Column(
        DateTime(),
        default=datetime.utcnow,
        nullable=False
    )
    type: MessageType = Column(
        Enum(MessageType),
        nullable=False
    )
    data: bytes = Column(
        LargeBinary(),
        nullable=True
    )

    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey('users.uuid'),
        nullable=False
    )
    room_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey('rooms.uuid'),
        nullable=False
    )
