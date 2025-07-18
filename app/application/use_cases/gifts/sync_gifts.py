from app.core.logger import logger
from app.interfaces.repositories import IGiftRepository
from app.interfaces.services.gifts_service import IGiftsService


class SyncGifts:
    def __init__(self, api: IGiftsService, repo: IGiftRepository):
        self.api = api
        self.repo = repo

    async def execute(self):
        logger.info("[UseCase:SyncGifts] Старт синхронизации подарков")
        gifts = await self.api.get_available_gifts() or None
        if not gifts:
            logger.warning("[UseCase:SyncGifts] Не удалось получить подарки или их нет")
            return
        logger.info(f"[UseCase:SyncGifts] Получено подарков: {len(gifts)}")
        await self.repo.save_all(gifts=gifts)
        logger.info("[UseCase:SyncGifts] Завершено")
