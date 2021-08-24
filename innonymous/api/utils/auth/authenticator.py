from typing import Callable, AsyncGenerator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from innonymous.api.utils.auth.i_authenticator import IAuthenticator
from innonymous.database.models import User
from innonymous.database.utils import get_by


class Authenticator(IAuthenticator):
    def __init__(
            self,
            session: Callable[[], AsyncGenerator[AsyncSession, None]]
    ) -> None:
        self.__session = session

    async def authenticate(self, uuid: UUID) -> User:
        user = None
        async for session in self.__session():
            user = await get_by(session, User, User.uuid, uuid)

        if not user:
            raise KeyError(
                f'Cannot find user with uuid {uuid}.'
            )

        return user[0]
