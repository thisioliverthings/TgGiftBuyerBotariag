from abc import ABC, abstractmethod

from app.domain.entities import AutoBuySettingDTO


class IAutoBuySettingRepository(ABC):
    @abstractmethod
    async def get_auto_buy_setting(self, telegram_id: int) -> AutoBuySettingDTO: ...
