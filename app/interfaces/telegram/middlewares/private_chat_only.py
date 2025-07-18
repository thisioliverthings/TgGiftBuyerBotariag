from aiogram import BaseMiddleware


class PrivateChatOnlyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        message = (
            data.get("event_update").message
            if hasattr(data.get("event_update"), "message")
            else None
        )
        if message and getattr(message.chat, "type", None) != "private":
            await message.answer("Бот работает только в личных сообщениях.")
            return
        callback_query = (
            data.get("event_update").callback_query
            if hasattr(data.get("event_update"), "callback_query")
            else None
        )
        if (
            callback_query
            and getattr(callback_query.message.chat, "type", None) != "private"
        ):
            await callback_query.answer(
                "Бот работает только в личных сообщениях.", show_alert=True
            )
            return
        return await handler(event, data)
