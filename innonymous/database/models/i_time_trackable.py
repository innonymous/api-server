from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime
)


class ITimeTrackable:
    def __init__(self, *args, **kwargs) -> None:
        pass

    active: datetime = Column(
        DateTime(), default=datetime.utcnow, nullable=False
    )
