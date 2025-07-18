from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.interfaces.telegram.messages import BUTTONS


def main_menu_keyboard(lang="ru", notifications_enabled: bool = True):
    notif_btn = (
        BUTTONS[lang]["notifications_on"]
        if notifications_enabled
        else BUTTONS[lang]["notifications_off"]
    )
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BUTTONS[lang]["balance"]),
                KeyboardButton(text=BUTTONS[lang]["buy_gift"]),
                KeyboardButton(text=BUTTONS[lang]["deposit"]),
            ],
            [
                KeyboardButton(text=BUTTONS[lang]["auto_buy"]),
                KeyboardButton(text=BUTTONS[lang]["history"]),
            ],
            [
                KeyboardButton(text=notif_btn),
                KeyboardButton(text=BUTTONS[lang]["language"]),
            ],
        ],
        resize_keyboard=True,
    )


def back_keyboard(lang="ru"):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BUTTONS[lang]["back"])]], resize_keyboard=True
    )


def cancel_keyboard(lang="ru"):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BUTTONS[lang]["cancel"])]], resize_keyboard=True
    )


def history_keyboard(has_prev, has_next, lang="ru"):
    if lang not in BUTTONS:
        lang = "ru"
    row = []
    if has_prev:
        row.append(KeyboardButton(text=BUTTONS[lang]["prev"]))
    if has_next:
        row.append(KeyboardButton(text=BUTTONS[lang]["next"]))
    keyboard = [row] if row else []
    keyboard.append([KeyboardButton(text=BUTTONS[lang]["back"])])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def auto_buy_keyboard(lang="ru"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BUTTONS[lang]["auto_buy_toggle"]),
            ],
            [
                KeyboardButton(text=BUTTONS[lang]["auto_buy_price"]),
                KeyboardButton(text=BUTTONS[lang]["auto_buy_supply"]),
                KeyboardButton(text=BUTTONS[lang]["auto_buy_cycles"]),
            ],
            [
                KeyboardButton(text=BUTTONS[lang]["back"]),
            ],
        ],
        resize_keyboard=True,
    )
