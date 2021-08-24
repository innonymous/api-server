from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from innonymous.database.models import Base


class Room(Base):
    __tablename__ = 'rooms'

    uuid: UUID = Column(
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True
    )
    name: str = Column(
        String(length=32),
        nullable=False
    )
    active: datetime = Column(
        DateTime(),
        default=datetime.utcnow,
        nullable=False
    )

    messages = relationship('Message', back_populates='room')
