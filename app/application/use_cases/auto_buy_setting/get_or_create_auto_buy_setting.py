from app.domain.entities import AutoBuySettingDTO
from app.interfaces.repositories import IAutoBuySettingRepository


class GetOrCreateAutoBuySetting:
    def __init__(self, repo: IAutoBuySettingRepository):
        self.repo = repo

    async def execute(self, telegram_id: int, user_id: int) -> AutoBuySettingDTO:
        setting = await self.repo.get_auto_buy_setting(telegram_id)
        if setting:
            return setting
        return await self.repo.create_auto_buy_setting(user_id)
