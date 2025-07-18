from aiogram import BaseMiddleware
from aiogram.exceptions import (
    TelegramForbiddenError,
    TelegramBadRequest,
    TelegramRetryAfter,
    TelegramAPIError,
    TelegramNetworkError,
    TelegramConflictError,
    TelegramUnauthorizedError,
    TelegramMigrateToChat,
)
from app.core.logger import logger


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except TelegramForbiddenError as e:
            user_id = self._get_user_id(event)
            logger.warning(f"Bot was blocked by user {user_id}: {e}")
            return
        except TelegramBadRequest as e:
            user_id = self._get_user_id(event)
            logger.warning(f"Bad request for user {user_id}: {e}")
            return
        except TelegramRetryAfter as e:
            user_id = self._get_user_id(event)
            logger.warning(
                f"Rate limit hit for user {user_id}, retry after {e.retry_after}s: {e}"
            )
            return
        except TelegramUnauthorizedError as e:
            logger.error(f"Bot token is invalid or bot was deleted: {e}")
            return
        except TelegramMigrateToChat as e:
            logger.warning(f"Chat migrated to {e.migrate_to_chat_id}: {e}")
            return
        except TelegramConflictError as e:
            user_id = self._get_user_id(event)
            logger.warning(f"Conflict error for user {user_id}: {e}")
            return
        except TelegramNetworkError as e:
            logger.error(f"Network error: {e}")
            return
        except TelegramAPIError as e:
            user_id = self._get_user_id(event)
            logger.error(f"Telegram API error for user {user_id}: {e}")
            return
        except Exception as e:
            user_id = self._get_user_id(event)
            logger.error(
                f"Unhandled exception for user {user_id} in {handler.__name__}: {e}"
            )
            return

    def _get_user_id(self, event):
        if hasattr(event, "from_user") and event.from_user:
            return event.from_user.id
        elif hasattr(event, "message") and event.message and event.message.from_user:
            return event.message.from_user.id
        elif (
            hasattr(event, "callback_query")
            and event.callback_query
            and event.callback_query.from_user
        ):
            return event.callback_query.from_user.id
        elif hasattr(event, "chat") and event.chat:
            return event.chat.id
        return None
