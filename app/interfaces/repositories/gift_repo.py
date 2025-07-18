from abc import ABC, abstractmethod
from typing import Sequence

from app.domain.entities import GiftDTO


class IGiftRepository(ABC):
    @abstractmethod
    async def save_all(self, gifts: Sequence[GiftDTO]) -> None: ...

    @abstractmethod
    async def get_new_gifts(self) -> list[GiftDTO]: ...

    @abstractmethod
    async def reset_new_gifts(self): ...
