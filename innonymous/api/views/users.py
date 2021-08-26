from uuid import UUID

from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api import db_engine, auth, captcha
from innonymous.api.schemas.token import TokenInfoSchema, TokenAuthPayloadSchema
from innonymous.api.schemas.token.payload import TokenCreatePayloadSchema
from innonymous.api.schemas.user import UserInfoSchema, UserCreateSchema, \
    UserConfirmSchema
from innonymous.database.models import User
from innonymous.database.utils import get_by

router = APIRouter(tags=['users'])


@router.get(
    '/users/{uuid}',
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
    '/users/new',
    response_model=UserConfirmSchema
)
async def create(
        user: UserCreateSchema
):
    # noinspection Pydantic
    payload = TokenCreatePayloadSchema(
        captcha=await captcha.generate(),
        **user.dict()
    )

    return UserConfirmSchema(
        captcha=payload.captcha,
        create_token=auth.encode(payload)
    )


@router.post(
    '/users/new/confirm',
    response_model=TokenInfoSchema
)
async def confirm(
        user: UserConfirmSchema,
        session: AsyncSession = Depends(db_engine.session)
) -> TokenInfoSchema:
    try:
        payload = auth.decode(
            user.create_token,
            TokenCreatePayloadSchema
        )

    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid or expired token.'
        ) from exc

    if not captcha.validate(payload.captcha, user.captcha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid captcha.'
        )

    _user = User(
        name=payload.name
    )

    session.add(_user)

    await session.commit()
    await session.refresh(_user)

    return TokenInfoSchema(
        access_token=auth.encode(
            TokenAuthPayloadSchema(
                uuid=_user.uuid
            )
        )
    )
