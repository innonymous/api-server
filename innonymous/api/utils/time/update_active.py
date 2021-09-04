from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.database.models import ITimeTrackable


async def update_active(model: ITimeTrackable, session: AsyncSession) -> None:
    model.active = datetime.utcnow()
    session.add(model)

    await session.commit()
