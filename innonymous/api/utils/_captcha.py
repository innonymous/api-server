import hmac
from random import choices
from string import digits, ascii_lowercase

from captcha.image import ImageCaptcha


class Captcha:
    length = 4
    algorithm = 'SHA256'

    # a-z, 0-9, except similar characters.
    alphabet = ''.join(
        set(ascii_lowercase + digits).difference(set('9q0ocda17uv6b'))
    )

    def __init__(self, key: str) -> None:
        self.__key = key.encode()
        self.__image = ImageCaptcha()

    def generate(self) -> tuple[str, bytes]:
        payload = ''.join(choices(Captcha.alphabet, k=Captcha.length))

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
