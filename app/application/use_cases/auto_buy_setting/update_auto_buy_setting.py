from app.domain.entities import AutoBuySettingDTO
from app.interfaces.repositories import IAutoBuySettingRepository


class UpdateAutoBuySetting:
    def __init__(self, repo: IAutoBuySettingRepository):
        self.repo = repo

    async def execute(self, telegram_id: int, **kwargs) -> AutoBuySettingDTO:
        return await self.repo.update_auto_buy_setting(telegram_id, **kwargs)
