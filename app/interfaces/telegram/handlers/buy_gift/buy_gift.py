import aiohttp
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.core.logger import logger
from app.application.use_cases import PurchaseGift
from app.infrastructure.db.repositories import TransactionRepository, UserRepository
from app.infrastructure.db.session import get_db
from app.infrastructure.services import TelegramGiftsApi
from app.interfaces.telegram.keyboards.default import back_keyboard, main_menu_keyboard
from app.interfaces.telegram.messages import BUTTONS, ERRORS, MESSAGES
from app.interfaces.telegram.states.gift_state import GiftStates

router = Router()


@logger.catch
@router.message(
    F.text.in_(
        [
            BUTTONS["ru"]["buy_gift"],
            BUTTONS["en"]["buy_gift"],
        ]
    )
)
async def buy_gift_command(message: types.Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        gifts_api = TelegramGiftsApi(session)
        gifts = await gifts_api.get_available_gifts()

    async with get_db() as db_session:
        user_repo = UserRepository(db_session)
        user = await user_repo.get_user_by_telegram_id(message.from_user.id)
        lang = user.language if user else "ru"

    if not gifts:
        await message.answer(
            MESSAGES[lang]["history_empty"], reply_markup=main_menu_keyboard(
                lang=lang)
        )
        return

    gifts_sorted = sorted(gifts, key=lambda g: g.star_count, reverse=True)
    gift_descriptions = [
        f'Подарок: {gift.emoji}\nID: <code>{gift.gift_id}</code>\nЦена: {gift.star_count}⭐️\nДоступно: {gift.remaining_count or "∞"}/{gift.total_count or "∞"}'
        for gift in gifts_sorted
    ]

    await message.answer("\n\n".join(gift_descriptions), parse_mode="HTML")
    await message.answer(
        text=MESSAGES[lang]["buy_gift_prompt"](message.from_user.id),
        reply_markup=back_keyboard(lang=lang),
    )

    await state.set_state(GiftStates.waiting_for_gift_id)
    await state.update_data(prev_state=None)


@logger.catch
@router.message(StateFilter(GiftStates.waiting_for_gift_id))
async def process_gift_id_input(message: types.Message, state: FSMContext):
    async with get_db() as db_session:
        user_repo = UserRepository(db_session)
        user = await user_repo.get_user_by_telegram_id(message.from_user.id)
        lang = user.language if user else "ru"

    try:
        parts = message.text.split()
        if len(parts) != 3:
            await message.reply(
                MESSAGES[lang]["buy_gift_error_format"],
                reply_markup=back_keyboard(lang=lang),
            )
            return
        gift_id, user_id, gifts_count = map(int, parts)
    except Exception:
        await message.reply(
            MESSAGES[lang]["buy_gift_error_numbers"],
            reply_markup=back_keyboard(lang=lang),
        )
        return

    payload = f"gift_{gift_id}_to_{user_id}_count_{gifts_count}"

    async with get_db() as session, aiohttp.ClientSession() as http_session:
        user_repo = UserRepository(session)
        transaction_repo = TransactionRepository(session)
        gifts_api = TelegramGiftsApi(http_session)
        use_case = PurchaseGift(user_repo, transaction_repo, gifts_api)
        result = await use_case.execute(
            buyer_telegram_id=message.from_user.id,
            recipient_id=user_id,
            gift_id=gift_id,
            gifts_count=gifts_count,
            payload=payload,
        )

        if not result["ok"]:
            err = result["error"]
            if err == "user_not_found":
                await message.reply(
                    ERRORS[lang]["user_not_found"],
                    reply_markup=back_keyboard(lang=lang),
                )
            elif err == "gift_not_found":
                await message.reply(
                    ERRORS[lang]["gift_not_found"],
                    reply_markup=back_keyboard(lang=lang),
                )
            elif err == "not_enough_balance":
                required = result["required"]
                price = result["gift_price"]
                prices = [
                    types.LabeledPrice(
                        label=MESSAGES[lang]["deposit_success"](required),
                        amount=required,
                    )
                ]
                await message.answer_invoice(
                    title=MESSAGES[lang]["deposit_success"](required),
                    description=f"Для покупки нужно {price * gifts_count}⭐️, у тебя {price * gifts_count - required}⭐️.",
                    payload=payload,
                    currency="XTR",
                    prices=prices,
                    provider_token="",
                    reply_markup=None,
                )
                await state.clear()

            elif err == "debit_failed":
                await message.reply(
                    ERRORS[lang]["debit_failed"], reply_markup=back_keyboard(
                        lang=lang)
                )

            elif err == "gift_send_failed":
                await message.reply(
                    ERRORS[lang]["gift_send_failed"],
                    reply_markup=back_keyboard(lang=lang),
                )

            elif err == "transaction_failed":
                await message.reply(
                    ERRORS[lang]["transaction_failed"],
                    reply_markup=back_keyboard(lang=lang),
                )

            else:
                await message.reply(
                    ERRORS[lang]["unknown"], reply_markup=back_keyboard(
                        lang=lang)
                )
            return

        user = result["user"]
        await message.reply(
            MESSAGES[lang]["buy_gift_success"](user.balance),
            reply_markup=main_menu_keyboard(lang=lang),
        )
        await state.clear()
