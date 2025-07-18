from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery

from app.application.use_cases import GetUserByTelegramId
from app.core.logger import logger
from app.infrastructure.db.repositories import UserRepository
from app.infrastructure.db.session import get_db
from app.interfaces.telegram.keyboards.default import back_keyboard, main_menu_keyboard
from app.interfaces.telegram.messages import BUTTONS, ERRORS, MESSAGES
from app.interfaces.telegram.states.deposit_state import DepositStates

router = Router()


@logger.catch
@router.message(
    F.text.in_(
        [
            BUTTONS["ru"]["deposit"],
            BUTTONS["en"]["deposit"],
        ]
    )
)
async def deposit_command(message: Message, state: FSMContext) -> None:
    async with get_db() as session:
        repo = UserRepository(session)
        user = await GetUserByTelegramId(repo).execute(telegram_id=message.from_user.id)
        lang = user.language if user else "ru"
        if not user:
            await message.reply(
                ERRORS[lang]["user_not_found"],
                reply_markup=main_menu_keyboard(lang=lang),
            )
            return
        await message.answer(
            text=MESSAGES[lang]["deposit_prompt"](user.username, user.balance),
            reply_markup=back_keyboard(lang=lang),
        )
        await state.set_state(DepositStates.waiting_for_amount_deposit)
        await state.update_data(prev_state=None)


@logger.catch
@router.message(StateFilter(DepositStates.waiting_for_amount_deposit))
async def process_deposit_input(message: Message, state: FSMContext) -> None:
    async with get_db() as session:
        repo = UserRepository(session)
        user = await GetUserByTelegramId(repo).execute(telegram_id=message.from_user.id)
        lang = user.language if user else "ru"
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError:
        await message.answer(
            text=MESSAGES[lang]["deposit_error"], reply_markup=back_keyboard(
                lang=lang)
        )
        return
    payload = f"deposit_{amount}_to_{message.from_user.id}"
    logger.info(
        f"Создаю депозит на {amount} звёзд от пользователя: {message.from_user.id}"
    )
    prices = [
        LabeledPrice(label=MESSAGES[lang]
                     ["deposit_invoice_title"], amount=amount)
    ]
    await message.answer_invoice(
        title=MESSAGES[lang]["deposit_invoice_title"],
        description=MESSAGES[lang]["deposit_invoice_description"](amount),
        payload=payload,
        currency="XTR",
        prices=prices,
        provider_token="",
        reply_markup=None,
    )
    await state.clear()


@logger.catch
@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(ok=True)
