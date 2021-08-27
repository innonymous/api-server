import hmac
from os import urandom
from re import fullmatch
from typing import Union

from captcha.image import ImageCaptcha


class Captcha:
    algorithm = 'SHA256'

    def __init__(
            self,
            key: Union[str, bytes]
    ) -> None:
        if isinstance(key, str):
            # If it is a hex.
            if fullmatch(r'^(\s*([0-9a-fA-F]{2})+\s*)*$', key):
                self.__key = bytes.fromhex(key)

            else:
                self.__key = key.encode()

        else:
            self.__key = key

        self.__image = ImageCaptcha()

    def generate(self) -> tuple[str, bytes]:
        payload = urandom(4).hex()

        with self.__image.generate(payload, 'jpeg') as buffer:
            captcha = buffer.getvalue()

        return (
            self.__hash(payload),
            captcha
        )

    def validate(self, _hash, payload: str) -> bool:
        return _hash == self.__hash(payload)

    def __hash(self, payload: str) -> str:
        return hmac.digest(
            self.__key,
            payload.lower().replace(' ', '').encode(),
            Captcha.algorithm
        ).hex()
