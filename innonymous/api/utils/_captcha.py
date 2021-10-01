import hmac
import random
import string

from captcha.image import ImageCaptcha


class Captcha:
    length = 4
    algorithm = 'SHA256'
    ttl = 5 * 60  # in seconds


    def __init__(self, key: str) -> None:
        self.__key = key.encode()
        self.__image = ImageCaptcha()
        
        forbidden_symbols = '0ocda17uv6b'
        self.alphabet = [
            c for c in string.ascii_lowercase + string.digits 
            if c not in forbidden_symbols
        ]

    def _generate_string(self) -> str:
        return ''.join(random.choices(self.alphabet, k=Captcha.length))

    def generate(self) -> tuple[str, bytes]:
        payload = self._generate_string()

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
