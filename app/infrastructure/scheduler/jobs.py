import asyncio

import aiohttp
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.application.use_cases import AutoBuyGiftsForAllUsers, PurchaseGift, SyncGifts
from app.core.config import settings
from app.core.logger import logger
from app.infrastructure.db.repositories import (
    AutoBuySettingReporistory,
    GiftRepository,
    UserRepository,
    TransactionRepository,
)
from app.infrastructure.db.session import get_db
from app.infrastructure.services import TelegramGiftsApi


sync_lock = asyncio.Lock()
pending_sync = False


def schedule_sync_job(bot: Bot):
    scheduler = AsyncIOScheduler()

    async def sync_and_auto_buy_job():
        global pending_sync
        if sync_lock.locked():
            pending_sync = True
            logger.info("[Scheduler] Пропущен запуск: предыдущий цикл ещё не завершён.")
            return
        async with sync_lock:
            try:
                async with get_db() as session:
                    async with aiohttp.ClientSession() as http_session:
                        gifts_api = TelegramGiftsApi(http_session)
                        gift_repo = GiftRepository(session)
                        user_repo = UserRepository(session)
                        auto_buy_repo = AutoBuySettingReporistory(session)
                        transaction_repo = TransactionRepository(session)
                        logger.info("[Scheduler] Запуск синхронизации подарков...")
                        sync_uc = SyncGifts(gifts_api, gift_repo)
                        await sync_uc.execute()
                        logger.info("[Scheduler] Синхронизация подарков завершена.")
                        new_gifts = await gift_repo.get_new_gifts()
                        if new_gifts:
                            logger.info(
                                f"[Scheduler] Найдено новых подарков: {len(new_gifts)}. Запуск автопокупки..."
                            )
                            purchase_uc = PurchaseGift(
                                user_repo, transaction_repo, gifts_api
                            )
                            auto_buy_uc = AutoBuyGiftsForAllUsers(
                                user_repo,
                                auto_buy_repo,
                                gift_repo,
                                gifts_api,
                                purchase_uc,
                                transaction_repo,
                                bot,
                            )
                            await auto_buy_uc.execute()
                            logger.info("[Scheduler] Автопокупка завершена.")
                        else:
                            logger.info(
                                "[Scheduler] Новых подарков нет. Автопокупка не требуется."
                            )
            except Exception as e:
                logger.error(f"[Scheduler] Ошибка в job: {e}")

            if pending_sync:
                pending_sync = False
                logger.info("[Scheduler] Запуск пропущенного sync_and_auto_buy_job...")
                await sync_and_auto_buy_job()

    scheduler.add_job(
        func=sync_and_auto_buy_job,
        trigger=IntervalTrigger(seconds=settings.check_gifts_delay_seconds),
        id="sync_and_auto_buy",
        replace_existing=True,
    )
    logger.info("[Scheduler] Планировщик запущен.")
    scheduler.start()
    return scheduler
