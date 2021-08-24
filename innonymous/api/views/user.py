from uuid import UUID

from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api import db_engine, auth
from innonymous.api.schemas.token import TokenInfoSchema, TokenPayloadSchema
from innonymous.api.schemas.user import UserInfoSchema, UserCreateSchema
from innonymous.database.models import User
from innonymous.database.utils import get_by

router = APIRouter(tags=['user'])


@router.get(
    '/user/{uuid}',
    response_model=UserInfoSchema
)
async def get(
        uuid: UUID,
        session: AsyncSession = Depends(db_engine.session)
) -> UserInfoSchema:
    user = await get_by(session, User, User.uuid, uuid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with uuid {uuid} not found.'
        )

    return UserInfoSchema.from_orm(
        user[0]
    )


@router.post(
    '/user/',
    response_model=TokenInfoSchema
)
async def create(
        user: UserCreateSchema,
        session: AsyncSession = Depends(db_engine.session)
) -> TokenInfoSchema:
    user = User(
        name=user.name
    )

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return TokenInfoSchema(
        access_token=auth.token(
            TokenPayloadSchema(
                uuid=user.uuid
            )
        )
    )
