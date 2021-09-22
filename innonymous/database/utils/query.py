from typing import (
    Any,
    TypeVar,
    Union
)

from sqlalchemy import (
    Column,
    asc,
    desc
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    Query,
    selectinload
)

from innonymous.database.models import Base

Model = TypeVar('Model', bound=Base)


async def query(
        session: AsyncSession,
        _query: Query,
        *,
        offset: int = None,
        limit: int = None,
        order_by: Union[Column, Any] = None,
        decreasing: bool = False,
        filters: list[Any] = None,
        fields_to_load: list[Union[Column, Any]] = None
) -> list[Model]:
    if fields_to_load:
        for field in fields_to_load:
            _query = _query.options(selectinload(field))

    if filters:
        for f in filters:
            _query = _query.filter(f)

    if order_by:
        if decreasing:
            order_by = desc(order_by)

        else:
            order_by = asc(order_by)

        _query = _query.order_by(order_by)

    if offset:
        _query = _query.offset(offset)

    if limit:
        _query = _query.limit(limit)

    return (await session.execute(_query)).scalars().all()
