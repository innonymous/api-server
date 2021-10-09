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
    db_engine,
    settings,
    mq
)
from innonymous.api.schemas.message import MessageInfoSchema
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
    UserModel,
    MessageModel,
    MessageType
)
from innonymous.api.docs.views import rooms as docs
from innonymous.database.utils import get_all, get_by

router = APIRouter(tags=['rooms'])


@router.get(
    '/rooms',
    response_model=RoomListSchema,
    description=docs.get.description
)
async def get(
        session: AsyncSession = Depends(db_engine.session)
) -> RoomListSchema:
    return RoomListSchema(
        rooms=[
            RoomInfoSchema.from_orm(room)
            for room in await get_all(session, RoomModel)
        ]
    )


@router.get(
    '/rooms/{uuid}',
    response_model=RoomInfoSchema,
    description=docs.get_by_uuid.description,
    responses=docs.get_by_uuid.responses
)
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


@router.post(
    '/rooms/new',
    response_model=RoomInfoSchema,
    description=docs.create.description,
    responses=docs.create.responses
)
async def create(
        room: RoomCreateSchema,
        user: UserModel = Depends(auth.authenticate),
        session: AsyncSession = Depends(db_engine.session)
) -> RoomInfoSchema:
    if inactivity_interval(user).total_seconds() < settings.minimal_delay:
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

    message = MessageModel(
        type=MessageType.text, data=b'Room created.', user=user, room=room
    )

    session.add(message)
    await session.commit()
    await mq.publish(MessageInfoSchema.from_orm(message))

    return RoomInfoSchema.from_orm(room)
