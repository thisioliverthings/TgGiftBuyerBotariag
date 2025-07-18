from aiogram.fsm.state import State, StatesGroup


class AutoBuyStates(StatesGroup):
    menu = State()
    set_price = State()
    set_supply = State()
    set_cycles = State()
