from aiogram import Router, types
from aiogram.filters import Command

from app.infrastructure.db.repositories import UserRepository
from app.infrastructure.db.session import get_db
from app.interfaces.telegram.keyboards.default import main_menu_keyboard
from app.interfaces.telegram.messages import MESSAGES

router = Router()


@router.message(Command(commands=["help"]))
async def help_command(message: types.Message):
    async with get_db() as session:
        repo = UserRepository(session)
        user = await repo.get_user_by_telegram_id(message.from_user.id)
        lang = user.language if user else "ru"
        await message.reply(
            text=MESSAGES[lang]["help"], reply_markup=main_menu_keyboard()
        )
