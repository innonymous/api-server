from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from innonymous.database.models import Base


class Room(Base):
    __tablename__ = 'rooms'

    uuid: UUID = Column(
        UUID(as_uuid=True),
        primary_key=True
    )
    name: str = Column(
        String(length=32),
        nullable=False
    )
