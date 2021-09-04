from datetime import (
    datetime,
    timedelta
)

from innonymous.api.utils.time.to_utc_native import to_utc_native
from innonymous.database.models import ITimeTrackable


def inactivity_interval(model: ITimeTrackable) -> timedelta:
    return datetime.utcnow() - to_utc_native(model.active)
