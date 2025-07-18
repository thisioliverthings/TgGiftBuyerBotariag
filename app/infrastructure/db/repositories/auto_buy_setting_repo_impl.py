from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.domain.entities import AutoBuySettingDTO
from app.infrastructure.db.models import AutoBuySettingModel, UserModel
from app.interfaces.repositories import IAutoBuySettingRepository


class AutoBuySettingReporistory(IAutoBuySettingRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @logger.catch
    async def get_auto_buy_setting(self, telegram_id: int) -> AutoBuySettingDTO | None:
        setting = await self.session.scalar(
            select(AutoBuySettingModel)
            .join(UserModel, AutoBuySettingModel.user_id == UserModel.id)
            .where(UserModel.telegram_id == telegram_id)
        )
        if not setting:
            logger.info(
                f"[AutoBuySettingRepo] Нет настроек автопокупки для telegram_id={telegram_id}"
            )
            return None

        logger.info(
            f"[AutoBuySettingRepo] Получены настройки автопокупки для user_id={setting.user_id}"
        )

        return AutoBuySettingDTO(
            id=setting.id,
            user_id=setting.user_id,
            status=setting.status,
            price_limit_from=setting.price_limit_from,
            price_limit_to=setting.price_limit_to,
            supply_limit=setting.supply_limit,
            cycles=setting.cycles,
        )

    @logger.catch
    async def create_auto_buy_setting(self, user_id: int) -> AutoBuySettingDTO:
        setting = AutoBuySettingModel(user_id=user_id)
        self.session.add(setting)
        await self.session.flush()

        logger.info(
            f"[AutoBuySettingRepo] Созданы настройки автопокупки для user_id={user_id}"
        )

        return AutoBuySettingDTO(
            id=setting.id,
            user_id=setting.user_id,
            status=setting.status,
            price_limit_from=setting.price_limit_from,
            price_limit_to=setting.price_limit_to,
            supply_limit=setting.supply_limit,
            cycles=setting.cycles,
        )

    @logger.catch
    async def update_auto_buy_setting(
        self, telegram_id: int, **kwargs
    ) -> AutoBuySettingDTO | None:
        setting = await self.session.scalar(
            select(AutoBuySettingModel)
            .join(UserModel, AutoBuySettingModel.user_id == UserModel.id)
            .where(UserModel.telegram_id == telegram_id)
        )
        if not setting:
            logger.info(
                f"[AutoBuySettingRepo] Не найдено настроек для обновления telegram_id={telegram_id}"
            )
            return None
        for key, value in kwargs.items():
            if hasattr(setting, key):
                setattr(setting, key, value)
        await self.session.flush()

        logger.info(
            f"[AutoBuySettingRepo] Обновлены настройки автопокупки для user_id={setting.user_id}: {kwargs}"
        )

        return AutoBuySettingDTO(
            id=setting.id,
            user_id=setting.user_id,
            status=setting.status,
            price_limit_from=setting.price_limit_from,
            price_limit_to=setting.price_limit_to,
            supply_limit=setting.supply_limit,
            cycles=setting.cycles,
        )
