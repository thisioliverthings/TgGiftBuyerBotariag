from aiogram import F, Router
from aiogram.types import Message

from app.core.logger import logger
from app.infrastructure.db.session import get_db
from app.interfaces.telegram.handlers.payment.deposit_payment import (
    process_deposit_payment,
)
from app.interfaces.telegram.handlers.payment.gift_payment import process_gift_payment

router = Router()


@logger.catch
@router.message(F.successful_payment)
async def handle_successful_payment(message: Message):
    payment_info = message.successful_payment

    logger.info(f"Успешная транзакция: {payment_info}")

    payload = payment_info.invoice_payload
    async with get_db() as session:
        if payload.startswith("deposit_"):
            try:
                await process_deposit_payment(message, payment_info, session)
            except ValueError:
                await message.answer(
                    "Произошла ошибка при депозите!\nПопробуйте позже."
                )

        elif payload.startswith("gift_"):
            try:
                await process_gift_payment(message, payment_info, session)
            except ValueError:
                await message.answer(
                    "Произошла ошибка при покупке подарков!\nПопробуйте позже."
                )

        else:
            logger.error(f"Неизвестный тип транзакции: {payload}")
            await message.answer(
                "Непредвиденная ошибка! Пожалуйста, свяжитесь с разработчиком!"
            )
