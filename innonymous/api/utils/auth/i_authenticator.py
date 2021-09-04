from abc import (
    ABC,
    abstractmethod
)
from typing import Any


class IAuthenticator(ABC):
    @abstractmethod
    def authenticate(self, *args, **kwargs) -> Any:
        pass
