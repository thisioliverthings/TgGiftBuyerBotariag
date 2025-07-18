from aiogram import Router, types
from aiogram.filters import CommandStart

from app.core.logger import logger
from app.interfaces.telegram.keyboards.inline import language_keyboard

router = Router()


@logger.catch
@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Выберите язык / Choose language:", reply_markup=language_keyboard()
    )
