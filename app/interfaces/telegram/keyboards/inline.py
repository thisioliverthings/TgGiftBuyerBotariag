from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def payment_keyboard(price):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Оплатить {price}⭐️")


def language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(
                    text="🇬🇧 English", callback_data="lang_en"),
            ]
        ]
    )


def history_pagination_keyboard(has_prev: bool, has_next: bool, current_page: int, total_pages: int, lang: str = "ru"):
    builder = InlineKeyboardBuilder()

    if has_prev:
        builder.button(text="◀️ Назад",
                       callback_data=f"history_prev_{current_page}")
    if has_next:
        builder.button(text="Вперёд ▶️",
                       callback_data=f"history_next_{current_page}")

    return builder.as_markup()
