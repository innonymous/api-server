import hmac
from os import urandom
from pathlib import Path
from re import fullmatch
from typing import Union

import aiofiles
from captcha.image import ImageCaptcha


class Captcha:
    algorithm = 'SHA256'

    def __init__(
            self,
            key: Union[str, bytes],
            store: Union[str, Path] = '/tmp/captcha',
            width: int = 256,
            height: int = 128
    ) -> None:
        if isinstance(key, str):
            # If it is a hex.
            if fullmatch(r'^(\s*([0-9a-fA-F]{2})+\s*)*$', key):
                self.__key = bytes.fromhex(key)
            else:
                self.__key = key.encode()

        else:
            self.__key = key

        self.__root = Path(store)
        self.__image = ImageCaptcha(
            width=width, height=height
        )

    async def generate(self) -> str:
        payload = urandom(4).hex()
        _hash = self.__hash(payload)

        async with aiofiles.open(self.__root / f'{_hash}', 'wb') as file:
            with self.__image.generate(payload, 'jpeg') as image:
                await file.write(image.getvalue())

        return _hash

    def validate(self, _hash, payload: str) -> bool:
        return _hash == self.__hash(payload)

    def __hash(self, payload: str) -> str:
        return hmac.digest(
            self.__key,
            payload.lower().replace(' ', '').encode(),
            Captcha.algorithm
        ).hex()
