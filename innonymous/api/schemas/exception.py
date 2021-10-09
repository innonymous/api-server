from pydantic import (
    BaseModel,
    Extra
)


class HTTPExceptionSchema(BaseModel):
    detail: str

    class Config:
        extra = Extra.forbid
