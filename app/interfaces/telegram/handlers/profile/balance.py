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
            BUTTONS["ru"]["balance"],
            BUTTONS["en"]["balance"],
        ]
    )
)
async def get_balance_command(message: Message) -> None:
    async with get_db() as session:
        repo = UserRepository(session)
        user = await GetUserByTelegramId(repo).execute(telegram_id=message.from_user.id)
        lang = user.language if user else "ru"
        await message.answer(
            MESSAGES[lang]["main_menu_balance"](user.username, user.balance),
            reply_markup=main_menu_keyboard(
                lang=lang, notifications_enabled=user.notifications_enabled
            ),
        )
