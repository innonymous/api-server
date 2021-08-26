from pathlib import Path
from typing import Type

from pydantic import BaseSettings, validator


class APISettings(BaseSettings):
    key: str
    database_url: str
    captcha_store: Path = '/tmp/captcha'

    @validator('key')
    def validate_key(cls: Type['APISettings'], value: str) -> str:
        if len(value) < 32:
            raise ValueError('Key should be at least 32 bytes long.')

        return value

    @validator('captcha_store')
    def validate_captcha_store(cls: Type['APISettings'], value: Path) -> Path:
        value.mkdir(parents=True, exist_ok=True)

        return value

    class Config:
        case_sensitive = False

        env_file = '.env'
        env_prefix = 'API_'
