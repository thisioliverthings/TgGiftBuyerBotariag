import aiohttp
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.application.use_cases import RefundTransaction
from app.core.logger import logger
from app.infrastructure.db.repositories import TransactionRepository, UserRepository
from app.infrastructure.db.session import get_db
from app.infrastructure.services import TelegramGiftsApi
from app.interfaces.telegram.keyboards.default import back_keyboard, main_menu_keyboard
from app.interfaces.telegram.messages import ERRORS, MESSAGES

router = Router(name="Refund router")


@logger.catch
@router.message(Command(commands=["refund"]))
async def command_refund_handler(message: Message) -> None:
    parts = message.text.strip().split()

    async with get_db() as session:
        user_repo = UserRepository(session)
        transaction_repo = TransactionRepository(session)

        user = await user_repo.get_user_by_telegram_id(message.from_user.id)
        lang = user.language if user else "ru"
        if len(parts) != 2:
            await message.reply(
                MESSAGES[lang]["input_error"], reply_markup=back_keyboard(lang=lang)
            )
            return

        transaction_id = parts[1]

        async with aiohttp.ClientSession() as http_session:
            gifts_api = TelegramGiftsApi(http_session)
            use_case = RefundTransaction(user_repo, transaction_repo, gifts_api)
            result = await use_case.execute(message.from_user.id, transaction_id)

        if not result["ok"]:
            err = result["error"]
            if err == "not_admin":
                await message.reply(
                    ERRORS[lang]["refund_not_admin"],
                    reply_markup=back_keyboard(lang=lang),
                )

            elif err == "transaction_not_found":
                await message.reply(
                    ERRORS[lang]["refund_not_found"],
                    reply_markup=back_keyboard(lang=lang),
                )

            elif err == "already_refunded":
                await message.reply(
                    ERRORS[lang]["refund_already"],
                    reply_markup=back_keyboard(lang=lang),
                )

            elif err == "user_not_found":
                await message.reply(
                    ERRORS[lang]["refund_user_not_found"],
                    reply_markup=back_keyboard(lang=lang),
                )

            elif err == "debit_failed":
                await message.reply(
                    ERRORS[lang]["refund_debit_failed"],
                    reply_markup=back_keyboard(lang=lang),
                )

            elif err == "telegram_refund_failed":
                await message.reply(
                    ERRORS[lang]["refund_telegram_failed"],
                    reply_markup=back_keyboard(lang=lang),
                )

            else:
                await message.reply(
                    f"{MESSAGES[lang]['operation_failed']} {err}",
                    reply_markup=back_keyboard(lang=lang),
                )

            return
        if user.notifications_enabled:
            await message.reply(
                MESSAGES[lang]["refund_success"](
                    transaction_id, result["refund_amount"]
                ),
                reply_markup=main_menu_keyboard(lang=lang),
            )
