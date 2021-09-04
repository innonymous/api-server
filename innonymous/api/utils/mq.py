from asyncio.exceptions import TimeoutError
from typing import (
    AsyncGenerator,
    Type,
    TypeVar
)

from aio_pika import (
    Channel,
    Exchange,
    ExchangeType,
    Message,
    RobustConnection,
    connect_robust
)


class MessageQueue:
    MessageSchema = TypeVar('MessageSchema')

    # noinspection PydanticTypeChecker
    def __init__(self, url: str):
        self.__url = url

        # Control.
        self.__channel: Channel = None
        self.__main_exchange: Exchange = None
        self.__connection: RobustConnection = None

    async def initialize(self) -> None:
        self.__connection: RobustConnection = await connect_robust(self.__url)
        self.__channel: Channel = await self.__connection.channel()

        self.__main_exchange = await self.__channel.declare_exchange(
            name='main', type=ExchangeType.FANOUT, durable=True
        )

    async def finalize(self) -> None:
        await self.__channel.close()
        await self.__connection.close()

    async def publish(self, message: MessageSchema) -> None:
        await self.__main_exchange.publish(
            Message(message.json().encode()), routing_key=''
        )

    async def subscribe(
            self, message_schema: Type[MessageSchema], timeout: int = 60
    ) -> AsyncGenerator[MessageSchema, None]:
        async with self.__connection.channel() as channel:
            queue = await channel.declare_queue(
                exclusive=True, auto_delete=True
            )

            await queue.bind(self.__main_exchange)

            try:
                message: Message
                async for message in queue.iterator(timeout=timeout):
                    yield message_schema.parse_raw(message.body.decode())

            except TimeoutError:
                return
