from typing import (
    Any,
    Type,
    TypeVar,
    Union
)

from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from innonymous.database.models import Base
from innonymous.database.utils.query import query

Model = TypeVar('Model', bound=Base)


async def get_by(
        session: AsyncSession,
        model: Type[Model],
        attribute: Union[Column, Any],
        value: Any,
        *args,
        **kwargs
) -> list[Model]:
    return await query(
        session, select(model).where(attribute == value), *args, **kwargs
    )
