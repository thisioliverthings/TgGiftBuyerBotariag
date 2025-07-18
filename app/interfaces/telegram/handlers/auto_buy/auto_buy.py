from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.application.use_cases import (
    GetOrCreateAutoBuySetting,
    GetUserByTelegramId,
    UpdateAutoBuySetting,
)
from app.core.logger import logger
from app.infrastructure.db.repositories import AutoBuySettingReporistory, UserRepository
from app.infrastructure.db.session import get_db
from app.interfaces.telegram.keyboards.default import (
    auto_buy_keyboard,
    back_keyboard,
    main_menu_keyboard,
)
from app.interfaces.telegram.messages import BUTTONS, ERRORS, MESSAGES
from app.interfaces.telegram.states.auto_buy_state import AutoBuyStates

router = Router()


@logger.catch
@router.message(
    F.text.in_(
        [
            BUTTONS["ru"]["auto_buy"],
            BUTTONS["en"]["auto_buy"],
        ]
    )
)
async def auto_buy_command(message: types.Message, state: FSMContext):
    async with get_db() as session:
        user_repo = UserRepository(session)
        auto_buy_repo = AutoBuySettingReporistory(session)
        user = await GetUserByTelegramId(user_repo).execute(message.from_user.id)
        lang = user.language if user else "ru"
        if not user:
            await message.answer(
                ERRORS[lang]["user_not_found"],
                reply_markup=main_menu_keyboard(lang=lang),
            )
            return
        settings = await GetOrCreateAutoBuySetting(auto_buy_repo).execute(
            message.from_user.id, user.id
        )
        await message.answer(
            text=MESSAGES[lang]["auto_buy_settings"](user, settings),
            reply_markup=auto_buy_keyboard(lang=lang),
            parse_mode="HTML",
        )
    await state.set_state(AutoBuyStates.menu)
    await state.update_data(prev_state=None)


@logger.catch
@router.message(StateFilter(AutoBuyStates.menu))
async def auto_buy_menu_handler(message: types.Message, state: FSMContext):
    async with get_db() as session:
        user_repo = UserRepository(session)
        auto_buy_repo = AutoBuySettingReporistory(session)
        user = await GetUserByTelegramId(user_repo).execute(message.from_user.id)
        lang = user.language if user else "ru"
        if not user:
            await message.answer(
                ERRORS[lang]["user_not_found"],
                reply_markup=main_menu_keyboard(lang=lang),
            )
            await state.clear()
            return
        settings = await GetOrCreateAutoBuySetting(auto_buy_repo).execute(
            message.from_user.id, user.id
        )
        if message.text in ["🔄 Вкл/Выкл автопокупку", "🔄 Toggle auto-buy"]:
            updated = await UpdateAutoBuySetting(auto_buy_repo).execute(
                message.from_user.id, status=not settings.status
            )
            await message.answer(
                f"{MESSAGES[lang]['auto_buy_status'](updated.status)}\n\n{MESSAGES[lang]['auto_buy_settings'](user, updated)}",
                reply_markup=auto_buy_keyboard(lang=lang),
                parse_mode="HTML",
            )
            await state.update_data(prev_state=None)
            return
        elif message.text in ["✏️ Лимит цены", "✏️ Price limit"]:
            await message.answer(
                text=MESSAGES[lang]["auto_buy_price_prompt"],
                reply_markup=back_keyboard(lang=lang),
                parse_mode="HTML",
            )
            await state.update_data(prev_state=AutoBuyStates.menu.state)
            await state.set_state(AutoBuyStates.set_price)
            return
        elif message.text in ["✏️ Лимит количества", "✏️ Supply limit"]:
            await message.answer(
                text=MESSAGES[lang]["auto_buy_supply_prompt"],
                reply_markup=back_keyboard(lang=lang),
                parse_mode="HTML",
            )
            await state.update_data(prev_state=AutoBuyStates.menu.state)
            await state.set_state(AutoBuyStates.set_supply)
            return
        elif message.text in ["✏️ Кол-во циклов", "✏️ Cycles"]:
            await message.answer(
                text=MESSAGES[lang]["auto_buy_cycles_prompt"],
                reply_markup=back_keyboard(lang=lang),
                parse_mode="HTML",
            )
            await state.update_data(prev_state=AutoBuyStates.menu.state)
            await state.set_state(AutoBuyStates.set_cycles)
            return
        await message.answer(
            text=MESSAGES[lang]["auto_buy_settings"](user, settings),
            reply_markup=auto_buy_keyboard(lang=lang),
            parse_mode="HTML",
        )
        await state.update_data(prev_state=None)


@logger.catch
@router.message(StateFilter(AutoBuyStates.set_price))
async def auto_buy_set_price_handler(message: types.Message, state: FSMContext):
    async with get_db() as session:
        user_repo = UserRepository(session)
        user = await GetUserByTelegramId(user_repo).execute(message.from_user.id)
        lang = user.language if user else "ru"
    try:
        price_limits = message.text.split()
        if len(price_limits) != 2:
            raise ValueError
        price_from, price_to = map(int, price_limits)
    except Exception:
        await message.answer(
            text=MESSAGES[lang]["auto_buy_price_error"],
            reply_markup=back_keyboard(lang=lang),
        )
        return
    async with get_db() as session:
        auto_buy_repo = AutoBuySettingReporistory(session)
        updated = await UpdateAutoBuySetting(auto_buy_repo).execute(
            message.from_user.id, price_limit_from=price_from, price_limit_to=price_to
        )
    await message.answer(
        f"{MESSAGES[lang]['auto_buy_price_set'](price_from, price_to)}\n\n{MESSAGES[lang]['auto_buy_settings'](user, updated)}",
        reply_markup=auto_buy_keyboard(lang=lang),
        parse_mode="HTML",
    )
    await state.set_state(AutoBuyStates.menu)
    await state.update_data(prev_state=None)


@logger.catch
@router.message(StateFilter(AutoBuyStates.set_supply))
async def auto_buy_set_supply_handler(message: types.Message, state: FSMContext):
    async with get_db() as session:
        user_repo = UserRepository(session)
        user = await GetUserByTelegramId(user_repo).execute(message.from_user.id)
        lang = user.language if user else "ru"
    try:
        supply_limit = int(message.text)
        if supply_limit <= 0:
            raise ValueError
    except Exception:
        await message.answer(
            text=MESSAGES[lang]["auto_buy_supply_error"],
            reply_markup=back_keyboard(lang=lang),
        )
        return
    async with get_db() as session:
        auto_buy_repo = AutoBuySettingReporistory(session)
        updated = await UpdateAutoBuySetting(auto_buy_repo).execute(
            message.from_user.id, supply_limit=supply_limit
        )
    await message.answer(
        f"{MESSAGES[lang]['auto_buy_supply_set'](supply_limit)}\n\n{MESSAGES[lang]['auto_buy_settings'](user, updated)}",
        reply_markup=auto_buy_keyboard(lang=lang),
        parse_mode="HTML",
    )
    await state.set_state(AutoBuyStates.menu)
    await state.update_data(prev_state=None)


@logger.catch
@router.message(StateFilter(AutoBuyStates.set_cycles))
async def auto_buy_set_cycles_handler(message: types.Message, state: FSMContext):
    async with get_db() as session:
        user_repo = UserRepository(session)
        user = await GetUserByTelegramId(user_repo).execute(message.from_user.id)
        lang = user.language if user else "ru"
    try:
        cycles = int(message.text)
        if cycles <= 0:
            raise ValueError
    except Exception:
        await message.answer(
            text=MESSAGES[lang]["auto_buy_cycles_error"],
            reply_markup=back_keyboard(lang=lang),
        )
        return
    async with get_db() as session:
        auto_buy_repo = AutoBuySettingReporistory(session)
        updated = await UpdateAutoBuySetting(auto_buy_repo).execute(
            message.from_user.id, cycles=cycles
        )
    await message.answer(
        f"{MESSAGES[lang]['auto_buy_cycles_set'](cycles)}\n\n{MESSAGES[lang]['auto_buy_settings'](user, updated)}",
        reply_markup=auto_buy_keyboard(lang=lang),
        parse_mode="HTML",
    )
    await state.set_state(AutoBuyStates.menu)
    await state.update_data(prev_state=None)
