from datetime import (
    datetime,
    timezone
)


def to_utc_native(_datetime: datetime) -> datetime:
    if _datetime.tzinfo:
        return _datetime.astimezone(timezone.utc).replace(tzinfo=None)

    return _datetime
