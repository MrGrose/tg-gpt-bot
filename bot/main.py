import asyncio
from bot.config import settings, SYSTEM_PROMPT
from bot.core.logger import logger
from bot.infrastructure.storage.memory_storage import MemoryStorage
from bot.infrastructure.llm.deepseek_provider import DeepSeekProvider
from bot.infrastructure.telegram.bot import create_bot
from bot.infrastructure.telegram.registration import setup_handlers
from bot.application.use_cases import ChatUseCase


async def main():
    logger.info("Бот запущен")
    storage = MemoryStorage()

    llm = DeepSeekProvider(settings.DEEPSEEK_API_KEY)
    logger.info("DeepSeekProvider запущен")

    chat_uc = ChatUseCase(storage=storage, llm=llm, system_prompt=SYSTEM_PROMPT)

    bot, dp = await create_bot(settings.BOT_TOKEN, settings.BOT_USERNAME)
    setup_handlers(dp, chat_uc)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
    finally:
        await llm.close()
        await bot.session.close()
        logger.info("Завершение работы")


if __name__ == "__main__":
    asyncio.run(main())
