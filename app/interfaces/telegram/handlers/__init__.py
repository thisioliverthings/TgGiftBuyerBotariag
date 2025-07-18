from aiogram import Dispatcher

from .help import router as help_router
from .start import router as start_router
from .auto_buy import auto_buy_router
from .buy_gift import buy_gift_router
from .payment import payment_handler_router
from .profile import (
    balance_router,
    deposit_router,
    refund_router,
    history_router,
    notifications_router,
    language_router,
)


def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(auto_buy_router)
    dp.include_router(buy_gift_router)
    dp.include_router(payment_handler_router)
    dp.include_router(balance_router)
    dp.include_router(deposit_router)
    dp.include_router(refund_router)
    dp.include_router(history_router)
    dp.include_router(notifications_router)
    dp.include_router(language_router)
