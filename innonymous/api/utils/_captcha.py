from hashlib import sha256
from os import urandom
from pathlib import Path
from typing import Union

import aiofiles
from captcha.image import ImageCaptcha


class Captcha:
    def __init__(
            self,
            key: str,
            store: Union[str, Path] = '/tmp/captcha',
            width: int = 256,
            height: int = 128
    ) -> None:
        self.__root = Path(store)
        self.__image = ImageCaptcha(
            width=width, height=height
        )

    async def generate(self) -> str:
        payload = urandom(4).hex()
        _hash = Captcha.__hash(payload)

        async with aiofiles.open(self.__root / f'{_hash}', 'wb') as file:
            with self.__image.generate(payload, 'jpeg') as image:
                await file.write(image.getvalue())

        return _hash


    def validate(self, _hash, payload: str) -> bool:
        return _hash == Captcha.__hash(payload)


    def __hash(self, payload: str):
        return sha256(
            payload.lower().replace(' ', '').encode()
        ).hexdigest()
