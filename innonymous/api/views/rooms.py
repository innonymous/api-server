from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api import (
    auth,
    db_engine
)
from innonymous.api.schemas.room import (
    RoomCreateSchema,
    RoomInfoSchema,
    RoomListSchema
)
from innonymous.api.utils.time import (
    inactivity_interval,
    update_active
)
from innonymous.database.models import (
    RoomModel,
    UserModel
)
from innonymous.database.utils import get_all, get_by

router = APIRouter(tags=['rooms'])


@router.get('/rooms', response_model=RoomListSchema)
async def get_all(
        session: AsyncSession = Depends(db_engine.session)
) -> RoomListSchema:
    return RoomListSchema(
        rooms=[
            RoomInfoSchema.from_orm(room)
            for room in await get_all(session, RoomModel)
        ]
    )


@router.get('/rooms/{uuid}', response_model=RoomInfoSchema)
async def get_by_uuid(
        uuid: UUID, session: AsyncSession = Depends(db_engine.session)
) -> RoomInfoSchema:
    room: RoomModel
    room, = await get_by(session, RoomModel, RoomModel.uuid, uuid) or [None]

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Room with uuid {uuid} not found.'
        )

    return RoomInfoSchema.from_orm(room)


@router.post('/rooms/new', response_model=RoomInfoSchema)
async def create(
        room: RoomCreateSchema,
        user: UserModel = Depends(auth.authenticate),
        session: AsyncSession = Depends(db_engine.session)
) -> RoomInfoSchema:
    if inactivity_interval(user).total_seconds() < 0.5:
        await update_active(user, session)

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail='Too many requests, try later.'
        )

    room = RoomModel(name=room.name)
    session.add(room)

    await session.commit()
    await session.refresh(room)
    await update_active(user, session)

    return RoomInfoSchema.from_orm(room)
