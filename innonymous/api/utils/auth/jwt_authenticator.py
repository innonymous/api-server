import json
from typing import (
    AsyncGenerator,
    Callable,
    Type,
    TypeVar
)

import jwt
from fastapi import (
    HTTPException,
    Security,
    status
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api.schemas.token.payload import TokenAuthPayloadSchema
from innonymous.api.utils.auth import IAuthenticator
from innonymous.api.utils.auth.authenticator import Authenticator
from innonymous.database.models import UserModel


class JWTAuthenticator(IAuthenticator):
    PayloadSchema = TypeVar('PayloadSchema', bound=BaseModel)

    algorithm = 'HS256'
    bearer = HTTPBearer()

    def __init__(
            self,
            key: str,
            session: Callable[[], AsyncGenerator[AsyncSession, None]]
    ) -> None:
        self.__key = key
        self.__authenticator = Authenticator(session)

    def encode(self, payload: PayloadSchema) -> str:
        payload = json.loads(payload.json())

        return jwt.encode(payload, self.__key, JWTAuthenticator.algorithm)

    def decode(self, token: str, model: Type[PayloadSchema]) -> PayloadSchema:
        return model.parse_obj(
            jwt.decode(token, self.__key, [JWTAuthenticator.algorithm, ])
        )

    async def authenticate(
            self, credentials: HTTPAuthorizationCredentials = Security(bearer)
    ) -> UserModel:
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid authorization code.'
            )

        if not credentials.scheme == 'Bearer':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid authentication scheme.'
            )

        try:
            payload = self.decode(
                credentials.credentials, TokenAuthPayloadSchema
            )

            return await self.__authenticator.authenticate(payload.uuid)

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid or expired token.'
            ) from exc
