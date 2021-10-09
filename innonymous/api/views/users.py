from base64 import b64encode
import time
from uuid import (
    UUID,
    uuid4
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api import (
    auth,
    captcha,
    db_engine,
    settings
)
from innonymous.api.schemas.token import TokenInfoSchema
from innonymous.api.schemas.token.payload import (
    TokenAuthPayloadSchema,
    TokenCreatePayloadSchema
)
from innonymous.api.schemas.user import (
    UserConfirmSchema,
    UserCreateSchema,
    UserInfoSchema
)
from innonymous.database.models import UserModel
from innonymous.database.utils import get_by
from innonymous.api.docs.views import users as docs

router = APIRouter(tags=['users'])


@router.get(
    '/users/{uuid}',
    response_model=UserInfoSchema,
    description=docs.get_by_uuid.description,
    responses=docs.get_by_uuid.responses
)
async def get_by_uuid(
        uuid: UUID, session: AsyncSession = Depends(db_engine.session)
) -> UserInfoSchema:
    user = await get_by(session, UserModel, UserModel.uuid, uuid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with uuid {uuid} not found.'
        )

    return UserInfoSchema.from_orm(user[0])


@router.post(
    '/users/new',
    response_model=UserConfirmSchema,
    description=docs.create.description
)
async def create(user: UserCreateSchema) -> UserConfirmSchema:
    _hash, _captcha = captcha.generate()

    # noinspection Pydantic
    payload = TokenCreatePayloadSchema(
        uuid=uuid4(), 
        captcha=_hash,
        exp=time.time() + settings.captcha_ttl,
        **user.dict(),
    )

    return UserConfirmSchema(
        captcha=b64encode(_captcha).decode(), create_token=auth.encode(payload)
    )


@router.post(
    '/users/new/confirm',
    response_model=TokenInfoSchema,
    description=docs.confirm.description,
    responses=docs.confirm.responses
)
async def confirm(
        user: UserConfirmSchema,
        session: AsyncSession = Depends(db_engine.session)
) -> TokenInfoSchema:
    try:
        payload = auth.decode(user.create_token, TokenCreatePayloadSchema)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid or expired token.'
        ) from exc

    if not captcha.validate(payload.captcha, user.captcha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid captcha.'
        )

    _user = await get_by(
        session, UserModel, UserModel.uuid, payload.uuid
    ) or None

    if _user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists.'
        )

    _user = UserModel(uuid=payload.uuid, name=payload.name)
    session.add(_user)

    await session.commit()
    await session.refresh(_user)

    return TokenInfoSchema(
        uuid=_user.uuid, access_token=auth.encode(
            TokenAuthPayloadSchema(uuid=_user.uuid)
        )
    )
