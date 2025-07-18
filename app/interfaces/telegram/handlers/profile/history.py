import datetime
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.application.use_cases import GetUserByTelegramId
from app.core.logger import logger
from app.infrastructure.db.repositories import TransactionRepository, UserRepository
from app.infrastructure.db.session import get_db
from app.interfaces.telegram.keyboards.default import (
    back_keyboard,
    main_menu_keyboard,
)
from app.interfaces.telegram.keyboards.inline import history_pagination_keyboard
from app.interfaces.telegram.messages import BUTTONS, MESSAGES


router = Router()


@logger.catch
@router.message(
    F.text.in_(
        [
            BUTTONS["ru"]["history"],
            BUTTONS["en"]["history"],
        ]
    )
)
async def history_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(history_page=0)
    await send_history_page(message, state)


@logger.catch
@router.callback_query(F.data.startswith("history_prev_"))
async def history_prev_callback(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    page = max(data.get("history_page", 0) - 1, 0)
    await state.update_data(history_page=page)
    await send_history_page(callback.message, state, callback.from_user.id)
    await callback.answer()


@logger.catch
@router.callback_query(F.data.startswith("history_next_"))
async def history_next_callback(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    page = data.get("history_page", 0) + 1
    await state.update_data(history_page=page)
    await send_history_page(callback.message, state, callback.from_user.id)
    await callback.answer()


async def send_history_page(message: Message, state: FSMContext, user_id: int = None):
    if user_id is None:
        user_id = message.from_user.id

    async with get_db() as session:
        repo = UserRepository(session)
        tx_repo = TransactionRepository(session)
        user = await GetUserByTelegramId(repo).execute(telegram_id=user_id)
        lang = user.language if user else "ru"
        data = await state.get_data()
        page = data.get("history_page", 0)
        limit = 5
        offset = page * limit

        total_transactions = await tx_repo.get_user_transactions_count(user.id)
        transactions = await tx_repo.get_user_transactions_paginated(
            user.id, offset, limit
        )

        total_pages = max(1, (total_transactions + limit - 1) // limit)
        has_next = page < total_pages - 1
        has_prev = page > 0

        if not transactions:
            await message.answer(
                MESSAGES[lang]["history_empty"],
                reply_markup=main_menu_keyboard(
                    lang=lang, notifications_enabled=user.notifications_enabled
                ),
            )
            return

        lines = []
        for tx in transactions:
            payload = tx.payload
            status = tx.status.name
            amount = tx.amount
            if payload and payload.startswith("deposit_"):
                op = MESSAGES[lang]["history_line_deposit_op"]
                emoji = "💳"
            elif payload and payload.startswith("gift_"):
                op = MESSAGES[lang]["history_line_gift_op"]
                emoji = "🎁"
            elif payload and payload.startswith("autobuy_"):
                op = MESSAGES[lang]["history_line_autobuy_op"]
                emoji = "🤖"
            elif status == "REFUNDED":
                op = MESSAGES[lang]["history_line_refund_op"]
                emoji = "↩️"
            else:
                op = MESSAGES[lang]["history_line_operation_op"]
                emoji = "💸"

            if status == "REFUNDED":
                tx_time = (
                    tx.updated_at.strftime("%Y-%m-%d %H:%M:%S") if tx.updated_at else ""
                )
            else:
                tx_time = (
                    tx.created_at.strftime("%Y-%m-%d %H:%M:%S") if tx.created_at else ""
                )

            line = f"{tx_time} | " + MESSAGES[lang]["history_line"](
                emoji, op, amount, status
            )
            lines.append(line)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"🕓 История\nВремя: {now}\nСтраница: {page+1}/{total_pages}\n"

        inline_markup = history_pagination_keyboard(
            has_prev, has_next, page, total_pages, lang
        )

        try:
            await message.edit_text(
                header + "\n" + "\n".join(lines),
                reply_markup=inline_markup,
            )
        except:
            await message.answer(
                header + "\n" + "\n".join(lines),
                reply_markup=inline_markup,
            )
