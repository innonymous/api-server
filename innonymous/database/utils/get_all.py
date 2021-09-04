from typing import (
    Type,
    TypeVar
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from innonymous.database.models import Base
from innonymous.database.utils.query import query

Model = TypeVar('Model', bound=Base)


async def get_all(
        session: AsyncSession, model: Type[Model], *args, **kwargs
) -> list[Model]:
    return await query(session, select(model), *args, **kwargs)
