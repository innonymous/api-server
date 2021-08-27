from typing import Type

from pydantic import BaseSettings, validator


class APISettings(BaseSettings):
    key: str
    database_url: str

    @validator('key')
    def validate_key(cls: Type['APISettings'], value: str) -> str:
        if len(value) < 32:
            raise ValueError('Key should be at least 32 bytes long.')

        return value

    class Config:
        case_sensitive = False

        env_file = '.env'
        env_prefix = 'API_'
