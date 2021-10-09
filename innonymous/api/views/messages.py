from datetime import datetime
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
    WebSocket
)
from sqlalchemy.ext.asyncio import AsyncSession
from websockets.exceptions import ConnectionClosedError

from innonymous.api import (
    auth,
    db_engine,
    mq,
    settings
)
from innonymous.api.schemas.message import (
    MessageCreateSchema,
    MessageInfoSchema,
    MessageListSchema
)
from innonymous.api.utils.time import (
    inactivity_interval,
    to_utc_native,
    update_active
)
from innonymous.database.models import (
    MessageModel,
    RoomModel,
    UserModel
)
from innonymous.api.docs.views import messages as docs
from innonymous.database.utils import get_by

router = APIRouter(tags=['messages'])


@router.get(
    '/rooms/{uuid}/messages',
    response_model=MessageListSchema,
    description=docs.get.description
)
async def get(
        uuid: UUID,
        limit: int = Query(100, gt=0, le=500),
        after: datetime = Query(None),
        before: datetime = Query(None),
        session: AsyncSession = Depends(db_engine.session)
) -> MessageListSchema:
    filters = []

    if after:
        filters.append(MessageModel.time >= to_utc_native(after))

    if before:
        filters.append(MessageModel.time <= to_utc_native(before))

    return MessageListSchema(
        messages=[
            MessageInfoSchema.from_orm(message)
            for message in await get_by(
                session,
                MessageModel,
                MessageModel.room_uuid,
                uuid,
                limit=limit,
                order_by=MessageModel.time,
                decreasing=True,
                filters=filters
            )
        ]
    )


@router.post(
    '/rooms/{uuid}/messages/new',
    description=docs.create.description,
    responses=docs.create.responses
)
async def create(
        uuid: UUID,
        message: MessageCreateSchema,
        user: UserModel = Depends(auth.authenticate),
        session: AsyncSession = Depends(db_engine.session)
) -> None:
    if inactivity_interval(user).total_seconds() < settings.minimal_delay:
        await update_active(user, session)

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail='Too many requests, try later.'
        )

    room: RoomModel
    room, = await get_by(session, RoomModel, RoomModel.uuid, uuid) or [None]

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Room with uuid {uuid} not found.'
        )

    message = MessageModel(
        type=message.type, data=message.data, user=user, room=room
    )

    session.add(message)

    await session.commit()
    await update_active(user, session)

    await mq.publish(MessageInfoSchema.from_orm(message))


@router.websocket('/messages/updates')
async def updates(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        async for message in mq.subscribe(MessageInfoSchema):
            await websocket.send_text(message.json())

    except ConnectionClosedError:
        return None

    finally:
        await websocket.close()
