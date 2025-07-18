import aiohttp

from app.core.logger import logger
from app.application.use_cases import PurchaseGift
from app.infrastructure.db.repositories import TransactionRepository, UserRepository
from app.infrastructure.services import TelegramGiftsApi
from app.interfaces.telegram.messages import ERRORS, MESSAGES


@logger.catch
async def process_gift_payment(message, payment_info, session, from_balance=False):
    if not from_balance:
        payload = payment_info.invoice_payload
        parts = payload.split("_")
        gift_id = int(parts[1])
        user_id = int(parts[3])
        gifts_count = int(parts[5])
        provider_charge_id = payment_info.telegram_payment_charge_id
    else:
        parts = message.text.split()
        gift_id = int(parts[0])
        user_id = int(parts[1])
        gifts_count = int(parts[2])
        payload = f"gift_{gift_id}_to_{user_id}_count_{gifts_count}"
        provider_charge_id = "buy_gift_transaction"

    async with aiohttp.ClientSession() as http_session:
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
            provider_charge_id=provider_charge_id,
        )

        user = result["user"] if result.get("user") else None
        lang = user.language if user else "ru"

        if not result["ok"]:
            err = result["error"]
            if err == "user_not_found":
                await message.reply(ERRORS[lang]["user_not_found"])

            elif err == "gift_not_found":
                await message.reply(ERRORS[lang]["gift_not_found"])

            elif err == "not_enough_balance":
                await message.reply(ERRORS[lang]["not_enough_balance"])

            elif err == "debit_failed":
                await message.reply(ERRORS[lang]["debit_failed"])

            elif err == "gift_send_failed":
                await message.reply(ERRORS[lang]["gift_send_failed"])

            elif err == "transaction_failed":
                await message.reply(ERRORS[lang]["transaction_failed"])

            else:
                await message.reply(ERRORS[lang]["unknown"])

            return
        if user and user.notifications_enabled:
            await message.reply(MESSAGES[lang]["buy_gift_success"](user.balance))
