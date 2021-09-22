import hmac
from os import urandom

from captcha.image import ImageCaptcha


class Captcha:
    length = 8
    algorithm = 'SHA256'

    def __init__(self, key: str) -> None:
        self.__key = key.encode()
        self.__image = ImageCaptcha()

    def generate(self) -> tuple[str, bytes]:
        payload = urandom((Captcha.length + 1) // 2).hex()

        with self.__image.generate(payload, 'jpeg') as buffer:
            captcha = buffer.getvalue()

        return self.__hash(payload), captcha

    def validate(self, _hash, payload: str) -> bool:
        return _hash == self.__hash(payload)

    def __hash(self, payload: str) -> str:
        return hmac.digest(
            self.__key,
            payload.lower().replace(' ', '').encode(),
            Captcha.algorithm
        ).hex()
