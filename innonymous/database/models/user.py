from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from innonymous.database.models import Base


class User(Base):
    __tablename__ = 'users'

    uuid: UUID = Column(
        UUID(as_uuid=True),
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
