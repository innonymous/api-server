import json
from typing import Callable, AsyncGenerator, TypeVar, Type

import jwt
from fastapi import status, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api.schemas.token import TokenAuthPayloadSchema
from innonymous.api.utils.auth.authenticator import Authenticator
from innonymous.database.models import User

PayloadSchema = TypeVar('PayloadSchema', bound=BaseModel)


class JWTAuthenticator(Authenticator):
    algorithm = 'HS256'
    bearer = HTTPBearer()

    def __init__(
            self,
            key: str,
            session: Callable[[], AsyncGenerator[AsyncSession, None]]
    ) -> None:
        super().__init__(session)

        self.__key = key

    def encode(self, payload: PayloadSchema) -> str:
        payload = json.loads(payload.json())

        return jwt.encode(
            payload,
            self.__key,
            JWTAuthenticator.algorithm
        )

    def decode(self, token: str, model: Type[PayloadSchema]) -> PayloadSchema:
        return model.parse_obj(
            jwt.decode(token, self.__key, [JWTAuthenticator.algorithm, ])
        )

    async def authenticate(
            self,
            credentials: HTTPAuthorizationCredentials = Security(bearer)
    ) -> User:
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
                credentials.credentials,
                TokenAuthPayloadSchema
            )

            return await super().authenticate(
                payload.uuid
            )

        except Exception as exc:
            from traceback import print_exc
            print_exc()

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid or expired token.'
            ) from exc
