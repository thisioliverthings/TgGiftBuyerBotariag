from aiogram.types import Message, SuccessfulPayment

from app.application.use_cases import CreateTransaction, CreditUserBalance
from app.core.logger import logger
from app.infrastructure.db.enums import TransactionStatus
from app.infrastructure.db.repositories import TransactionRepository, UserRepository
from app.interfaces.telegram.keyboards.default import main_menu_keyboard
from app.interfaces.telegram.messages import ERRORS, MESSAGES


@logger.catch
async def process_deposit_payment(
    message: Message, payment_info: SuccessfulPayment, session
) -> None:
    payload = payment_info.invoice_payload
    parts = payload.split("_")
    amount = int(parts[1])
    user_id = int(parts[3])

    user_repo = UserRepository(session)
    transaction_repo = TransactionRepository(session)
    user = await CreditUserBalance(user_repo).execute(
        telegram_id=user_id, amount=amount
    )
    lang = user.language if user else "ru"

    if not user:
        raise ValueError(ERRORS[lang]["user_not_found"])

    transaction = await CreateTransaction(transaction_repo).execute(
        user_id=user.id,
        amount=amount,
        telegram_payment_charge_id=payment_info.telegram_payment_charge_id,
        status=TransactionStatus.COMPLETED,
        payload=payload,
    )

    if not transaction:
        raise ValueError(ERRORS[lang]["transaction_failed"])

    if user.notifications_enabled:
        await message.answer(
            MESSAGES[lang]["deposit_success"](amount), reply_markup=main_menu_keyboard()
        )
