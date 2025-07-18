from abc import ABC, abstractmethod

from app.domain.entities import GiftDTO


class IGiftsService(ABC):
    @abstractmethod
    async def get_available_gifts(self) -> list[GiftDTO] | None: ...

    @abstractmethod
    async def send_gift(
        self, user_id: int, gift_id: str, pay_for_upgrade: bool = False
    ) -> bool: ...
