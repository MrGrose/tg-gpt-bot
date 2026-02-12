from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand


async def create_bot(token: str, username: str):
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Начать диалог"),
            BotCommand(command="new", description="Новый диалог"),
            BotCommand(command="help", description="Помощь"),
        ]
    )

    return bot, dp
