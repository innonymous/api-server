from datetime import datetime
from uuid import UUID

from fastapi import status, APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api import db_engine, auth
from innonymous.api.schemas.message import MessageListSchema, \
    MessageInfoSchema, MessageCreateSchema
from innonymous.api.utils import to_utc_native
from innonymous.database.models import Message, Room, User
from innonymous.database.utils import get_by

router = APIRouter(tags=['messages', 'rooms'])


@router.get(
    '/rooms/{uuid}/messages',
    response_model=MessageListSchema
)
async def get(
        uuid: UUID,
        limit: int = Query(
            None,
            gt=0
        ),
        after: datetime = Query(
            None
        ),
        before: datetime = Query(
            None
        ),
        session: AsyncSession = Depends(db_engine.session)
) -> MessageListSchema:
    filters = []
    if after:
        filters.append(Message.time >= to_utc_native(after))
    if before:
        filters.append(Message.time <= to_utc_native(before))

    return MessageListSchema(
        messages=[
            MessageInfoSchema.from_orm(room)
            for room in await get_by(
                session,
                Message,
                Message.room_uuid,
                uuid,
                limit=limit,
                order_by=Message.time,
                decreasing=True,
                filters=filters
            )
        ]
    )


@router.post(
    '/rooms/{uuid}/messages/new'
)
async def create(
        uuid: UUID,
        message: MessageCreateSchema,
        user: User = Depends(auth.authenticate),
        session: AsyncSession = Depends(db_engine.session)
) -> None:
    room: Room
    room, = await get_by(session, Room, Room.uuid, uuid) or [None]

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with uuid {uuid} not found.'
        )

    message = Message(
        type=message.type,
        data=message.data,
        user=user,
        room=room
    )

    # Last active.
    user.active = room.active = datetime.utcnow()

    session.add(user)
    session.add(room)
    session.add(message)

    await session.commit()
