from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker


class DatabaseEngine:
    def __init__(self, url: str) -> None:
        self.__db_engine = create_async_engine(url, future=True)

        self.__db_session_maker = sessionmaker(
            self.__db_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            future=True
        )

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__db_session_maker() as session:
            yield session

    async def finalize(self) -> None:
        await self.__db_engine.dispose()
