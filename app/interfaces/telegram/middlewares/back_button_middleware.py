from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.core.logger import logger
from app.interfaces.telegram.messages import BUTTONS, MESSAGES
from app.infrastructure.db.repositories import UserRepository, AutoBuySettingReporistory
from app.infrastructure.db.session import get_db
from app.interfaces.telegram.keyboards.default import (
    main_menu_keyboard,
    auto_buy_keyboard,
)
from app.interfaces.telegram.states.auto_buy_state import AutoBuyStates


class BackButtonMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            logger.info(
                f"BackButtonMiddleware: Processing message with text: '{event.text}'"
            )

            if event.text in [BUTTONS["ru"]["back"], BUTTONS["en"]["back"]]:
                logger.info(f"Back button detected: '{event.text}'")

                try:
                    state: FSMContext = data.get("state")
                    if not state:
                        logger.info("No state found, returning to main menu")
                        await self._return_to_main_menu(event)
                        return

                    current_state = await state.get_state()
                    data_state = await state.get_data()
                    prev_state = data_state.get("prev_state")

                    logger.info(
                        f"Current state: {current_state}, prev_state: {prev_state}"
                    )

                    if not current_state:
                        logger.info("No current state, returning to main menu")
                        await state.clear()
                        await self._return_to_main_menu(event)
                        return
                    elif current_state and current_state.startswith("AutoBuyStates"):
                        await self._handle_auto_buy_back(
                            event, state, current_state, prev_state
                        )
                        return
                    elif current_state and current_state.startswith("GiftStates"):
                        await state.clear()
                        await self._return_to_main_menu(event)
                        return
                    elif current_state and current_state.startswith("DepositStates"):
                        await state.clear()
                        await self._return_to_main_menu(event)
                        return
                    else:
                        if prev_state:
                            await state.set_state(prev_state)
                            if prev_state == AutoBuyStates.menu.state:
                                await self._return_to_auto_buy_menu(event)
                                return
                        else:
                            await state.clear()
                            await self._return_to_main_menu(event)
                            return
                except Exception as e:
                    logger.error(f"Error in back button middleware: {e}")
                    await self._return_to_main_menu(event)
                    return

        return await handler(event, data)

    async def _return_to_main_menu(self, event):
        async with get_db() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_user_by_telegram_id(event.from_user.id)
            lang = user.language if user else "ru"
            text = MESSAGES[lang]["onboarding"](
                user.username if user else "user", user.balance if user else 0
            )
            await event.answer(
                text,
                reply_markup=main_menu_keyboard(
                    lang=lang,
                    notifications_enabled=(
                        user.notifications_enabled if user else True
                    ),
                ),
            )

    async def _return_to_auto_buy_menu(self, event):
        async with get_db() as session:
            user_repo = UserRepository(session)
            auto_buy_repo = AutoBuySettingReporistory(session)
            user = await user_repo.get_user_by_telegram_id(event.from_user.id)
            settings = await auto_buy_repo.get_auto_buy_setting(event.from_user.id)
            lang = user.language if user else "ru"
            await event.answer(
                MESSAGES[lang]["auto_buy_settings"](user, settings),
                reply_markup=auto_buy_keyboard(lang=lang),
                parse_mode="HTML",
            )

    async def _handle_auto_buy_back(self, event, state, current_state, prev_state):
        if current_state == AutoBuyStates.menu.state:
            await state.clear()
            await self._return_to_main_menu(event)
        elif prev_state == AutoBuyStates.menu.state:
            await state.set_state(AutoBuyStates.menu)
            await state.update_data(prev_state=None)
            await self._return_to_auto_buy_menu(event)
        else:
            await state.clear()
            await self._return_to_main_menu(event)
