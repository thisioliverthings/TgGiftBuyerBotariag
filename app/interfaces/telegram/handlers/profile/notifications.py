from aiogram import Router, F
from aiogram.types import Message

from app.application.use_cases import GetUserByTelegramId
from app.core.logger import logger
from app.infrastructure.db.repositories import UserRepository
from app.infrastructure.db.session import get_db
from app.interfaces.telegram.keyboards.default import main_menu_keyboard
from app.interfaces.telegram.messages import BUTTONS, MESSAGES


router = Router()


@logger.catch
@router.message(
    F.text.in_(
        [
            BUTTONS["ru"]["notifications_on"],
            BUTTONS["en"]["notifications_on"],
            BUTTONS["ru"]["notifications_off"],
            BUTTONS["en"]["notifications_off"],
        ]
    )
)
async def toggle_notifications(message: Message):
    async with get_db() as session:
        repo = UserRepository(session)
        user = await GetUserByTelegramId(repo).execute(telegram_id=message.from_user.id)
        lang = user.language if user else "ru"
        enabled = await repo.get_notifications_enabled(message.from_user.id)
        await repo.set_notifications_enabled(message.from_user.id, not enabled)
        toggled_msg = MESSAGES[lang].get("notifications_toggled")
        if toggled_msg is None:
            toggled_msg = (
                "Уведомления включены."
                if not enabled
                else (
                    "Уведомления отключены."
                    if lang == "ru"
                    else (
                        "Notifications enabled."
                        if not enabled
                        else "Notifications disabled."
                    )
                )
            )
        else:
            toggled_msg = toggled_msg(
                "Уведомления включены." if not enabled else "Уведомления отключены."
            )
        await message.answer(
            toggled_msg,
            reply_markup=main_menu_keyboard(
                lang=lang, notifications_enabled=not enabled
            ),
        )
