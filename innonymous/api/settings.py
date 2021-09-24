from typing import Type, Optional

from pydantic import (
    BaseSettings,
    validator
)


class APISettings(BaseSettings):
    key: str
    amqp_url: str
    database_url: str

    # Root of the api endpoints.
    root_path: Optional[str]

    @validator('key')
    def validate_key(cls: Type['APISettings'], value: str) -> str:
        if len(value) < 32:
            raise ValueError('Key should be at least 32 bytes long.')

        return value

    class Config:
        case_sensitive = False

        env_file = '.env'
        env_prefix = 'API_'
