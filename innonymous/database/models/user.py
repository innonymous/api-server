from uuid import uuid4

from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from innonymous.database.models import Base
from innonymous.database.models.i_time_trackable import ITimeTrackable


class UserModel(Base, ITimeTrackable):
    __tablename__ = 'users'

    uuid: UUID = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name: str = Column(String(length=32), nullable=False)

    messages = relationship('MessageModel', back_populates='user')
