from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.application.use_cases import GetUserByTelegramId
from app.core.logger import logger
from app.infrastructure.db.repositories import UserRepository
from app.infrastructure.db.session import get_db
from app.interfaces.telegram.keyboards.default import main_menu_keyboard
from app.interfaces.telegram.keyboards.inline import language_keyboard
from app.interfaces.telegram.messages import BUTTONS, MESSAGES


router = Router()


@logger.catch
@router.message(
    F.text.in_(
        [
            BUTTONS["ru"]["language"],
            BUTTONS["en"]["language"],
        ]
    )
)
async def change_language(message: Message):
    async with get_db() as session:
        repo = UserRepository(session)
        user = await GetUserByTelegramId(repo).execute(telegram_id=message.from_user.id)
        lang = user.language if user else "ru"
        prompt = MESSAGES[lang].get("change_language_prompt")
        if prompt is None:
            prompt = "Выберите язык:" if lang == "ru" else "Choose language:"
        await message.answer(
            prompt,
            reply_markup=language_keyboard(),
        )


@router.callback_query(lambda c: c.data in ["lang_ru", "lang_en"])
async def set_language_callback(call: CallbackQuery):
    lang = "ru" if call.data == "lang_ru" else "en"
    async with get_db() as session:
        repo = UserRepository(session)
        user = await repo.get_user_by_telegram_id(call.from_user.id)
        if user:
            await repo.set_language(call.from_user.id, lang)
        else:
            user = await repo.create(
                call.from_user.id, call.from_user.username or "user", language=lang
            )
        onboarding_text = MESSAGES[lang]["onboarding"](
            user.username, user.balance)

        # Если это выбор языка при старте, удаляем сообщение и отправляем новое
        if call.message.text == "Выберите язык / Choose language:":
            await call.message.delete()
            await call.message.answer(
                onboarding_text,
                reply_markup=main_menu_keyboard(
                    lang=lang, notifications_enabled=user.notifications_enabled
                ),
            )
        else:
            # Если это смена языка из меню, редактируем текущее сообщение
            await call.message.edit_text(onboarding_text, reply_markup=language_keyboard())

        await call.answer()
