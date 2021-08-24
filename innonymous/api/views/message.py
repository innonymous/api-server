from uuid import UUID

from fastapi import status, APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api import db_engine, auth
from innonymous.api.schemas.message import MessageListSchema, \
    MessageInfoSchema, MessageCreateSchema
from innonymous.database.models import Message, Room, User
from innonymous.database.utils import get_by

router = APIRouter(tags=['messages', 'room'])


@router.get(
    '/room/{uuid}/messages',
    response_model=MessageListSchema
)
async def get(
        uuid: UUID,
        offset: int = Query(
            0,
            ge=0
        ),
        limit: int = Query(
            15,
            ge=1,
            le=100
        ),
        session: AsyncSession = Depends(db_engine.session)
) -> MessageListSchema:
    return MessageListSchema(
        messages=[
            MessageInfoSchema.from_orm(room)
            for room in await get_by(
                session,
                Message,
                Message.room_uuid,
                uuid,
                offset,
                limit,
                order_by=Message.time,
                decreasing=True
            )
        ]
    )


@router.post(
    '/room/{uuid}/message'
)
async def create(
        uuid: UUID,
        message: MessageCreateSchema,
        user: User = Depends(auth.authenticate),
        session: AsyncSession = Depends(db_engine.session)
) -> None:
    room = await get_by(session, Room, Room.uuid, uuid)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with uuid {uuid} not found.'
        )

    message = Message(
        type=message.type,
        data=message.data,
        user=user,
        room=room[0]
    )

    session.add(message)

    await session.commit()
