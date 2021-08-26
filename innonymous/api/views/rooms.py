from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api import db_engine, auth
from innonymous.api.schemas.room import RoomInfoSchema, RoomListSchema, \
    RoomCreateSchema
from innonymous.database.models import Room
from innonymous.database.utils import get_all

router = APIRouter(tags=['rooms'])


@router.get(
    '/rooms/',
    response_model=RoomListSchema
)
async def get(
        session: AsyncSession = Depends(db_engine.session)
) -> RoomListSchema:
    return RoomListSchema(
        rooms=[
            RoomInfoSchema.from_orm(room)
            for room in await get_all(session, Room)
        ]
    )


@router.post(
    '/rooms/new',
    response_model=RoomInfoSchema,
    dependencies=[
        Depends(auth.authenticate)
    ]
)
async def create(
        room: RoomCreateSchema,
        session: AsyncSession = Depends(db_engine.session)
) -> RoomInfoSchema:
    room = Room(
        name=room.name
    )

    session.add(room)

    await session.commit()
    await session.refresh(room)

    return RoomInfoSchema.from_orm(
        room
    )
