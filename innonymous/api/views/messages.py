from datetime import datetime
from uuid import UUID

from fastapi import status, APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api import db_engine, auth
from innonymous.api.schemas.message import MessageListSchema, \
    MessageInfoSchema, MessageCreateSchema
from innonymous.api.utils.time import to_utc_native, inactivity_interval, \
    update_active
from innonymous.database.models import MessageModel, RoomModel, UserModel
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
        filters.append(MessageModel.time >= to_utc_native(after))
    if before:
        filters.append(MessageModel.time <= to_utc_native(before))

    return MessageListSchema(
        messages=[
            MessageInfoSchema.from_orm(room)
            for room in await get_by(
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
    '/rooms/{uuid}/messages/new'
)
async def create(
        uuid: UUID,
        message: MessageCreateSchema,
        user: UserModel = Depends(auth.authenticate),
        session: AsyncSession = Depends(db_engine.session)
) -> None:
    if inactivity_interval(user).total_seconds() < 0.5:
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
            detail=f'UserModel with uuid {uuid} not found.'
        )

    message = MessageModel(
        type=message.type,
        data=message.data,
        user=user,
        room=room
    )

    session.add(message)

    await session.commit()
    await update_active(room, session)
    await update_active(user, session)
