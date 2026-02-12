import time
from aiogram.types import Message
from bot.config import settings, messages as msg
from bot.core.logger import logger


_rate_limit_storage = {}


async def validate_message_length(message: Message) -> bool:
    if len(message.text) > settings.MAX_MESSAGE_LENGTH:
        await message.answer(
            msg.TOO_LONG.format(sent=len(message.text), limit=settings.MAX_MESSAGE_LENGTH)
        )
        logger.warning(
            f"Пользователь {message.from_user.id} превысил лимит длины: "
            f"{len(message.text)}/{settings.MAX_MESSAGE_LENGTH} символов"
        )
        return False
    return True


async def validate_message_not_empty(message: Message) -> bool:
    if not message.text.strip():
        await message.answer(msg.EMPTY_MESSAGE)
        return False
    return True


async def check_rate_limit(user_id: int) -> bool:
    last_time = _rate_limit_storage.get(user_id, 0)
    now = time.time()

    if now - last_time < settings.RATE_LIMIT_SECONDS:
        logger.warning(
            f"Пользователь {user_id} слишком часто отправляет сообщения"
        )
        return False

    _rate_limit_storage[user_id] = now
    return True


def truncate_response(response: str) -> str:
    if len(response) > settings.MAX_RESPONSE_LENGTH:
        logger.info(
            f"Ответ обрезан: {len(response)} -> {settings.MAX_RESPONSE_LENGTH} символов"
        )
        return response[: settings.MAX_RESPONSE_LENGTH] + msg.TRUNCATED
    return response
