from aiogram import Router
from bot.application.use_cases import ChatUseCase
from bot.infrastructure.telegram.handlers import BotHandlers


def setup_handlers(router: Router, chat_uc: ChatUseCase):
    handlers = BotHandlers(chat_uc)
    router.include_router(handlers.router)
