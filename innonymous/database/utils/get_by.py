from typing import Any, Type, TypeVar

from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from innonymous.database.models import Base

Model = TypeVar('Model', bound=Base)


async def get_by(
        session: AsyncSession,
        model: Type[Model],
        attribute: Column,
        value: Any,
        *fields_to_load: Column
) -> Model:
    query = select(model).where(attribute == value)

    for field in fields_to_load:
        query = query.options(selectinload(field))

    return (
        await session.execute(query)
    ).scalar()
