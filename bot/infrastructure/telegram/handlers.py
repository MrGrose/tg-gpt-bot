from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from bot.application.use_cases import ChatUseCase
from bot.config import settings, messages as msg
from bot.core.logger import logger
from bot.infrastructure.telegram.utils import (
    validate_message_length,
    validate_message_not_empty,
    check_rate_limit,
    truncate_response,
)


class BotHandlers:
    def __init__(self, chat_uc: ChatUseCase):
        self.chat_uc = chat_uc
        self.router = Router()
        self._register_handlers()

    def _register_handlers(self):
        self.router.message.register(self.start, Command("start"))
        self.router.message.register(self.help, Command("help"))
        self.router.message.register(self.new_chat, Command("new"))
        self.router.message.register(self.handle_text, F.text)

    async def start(self, message: Message):
        try:
            self.chat_uc.clear_context(message.from_user.id)
            logger.info(f"Пользователь {message.from_user.id} начал новый чат")
            await message.answer(msg.WELCOME.format(name=message.from_user.first_name))
        except Exception as e:
            logger.error(f"Ошибка в обработчике /start: {e}", exc_info=True)
            await message.answer(msg.GENERIC_ERROR)

    async def help(self, message: Message):
        try:
            await message.answer(msg.HELP.format(limit=settings.MAX_MESSAGE_LENGTH))
            logger.info(f"Пользователь {message.from_user.id} запросил помощь")
        except Exception as e:
            logger.error(f"Ошибка в обработчике /help: {e}", exc_info=True)

    async def new_chat(self, message: Message):
        try:
            self.chat_uc.clear_context(message.from_user.id)
            logger.info(f"Пользователь {message.from_user.id} сбросил контекст через /new")
            await message.answer(
                msg.NEW_DIALOG.format(
                    name=message.from_user.first_name, limit=settings.MAX_MESSAGE_LENGTH
                )
            )
        except Exception as e:
            logger.error(f"Ошибка в обработчике /new: {e}", exc_info=True)
            await message.answer(msg.RESET_ERROR)

    async def handle_text(self, message: Message):
        if not await validate_message_length(message):
            return
        if not await validate_message_not_empty(message):
            return

        if not await check_rate_limit(message.from_user.id):
            await message.answer(msg.TOO_OFTEN)
            return

        await message.bot.send_chat_action(message.chat.id, "typing")

        try:
            response = await self.chat_uc.process_message(
                user_id=message.from_user.id, text=message.text
            )
            response = truncate_response(response)
            await message.answer(response)
            logger.info(f"Пользователь {message.from_user.id}: запрос обработан")

        except TelegramBadRequest as e:
            logger.error(f"Ошибка Telegram API: {e}", exc_info=True)
            await message.answer(msg.TELEGRAM_ERROR)
        except Exception as e:
            logger.error(f"Внутренняя ошибка от {message.from_user.id}: {e}", exc_info=True)
            await message.answer(msg.INTERNAL_ERROR)
