from bot.domain.interfaces import Storage, LLMProvider
from bot.core.logger import logger


class ChatUseCase:
    def __init__(self, storage: Storage, llm: LLMProvider, system_prompt: str):
        self.storage = storage
        self.llm = llm
        self.system_prompt = system_prompt

    async def process_message(self, user_id: int, text: str) -> str:
        try:
            dialog = self.storage.get_dialog(user_id)
            dialog.add_message("user", text)

            context = dialog.get_context()
            logger.debug(f"Пользователь {user_id}: контекст {len(context)} сообщений")

            response = await self.llm.generate(messages=context, system_prompt=self.system_prompt)

            dialog.add_message("assistant", response)
            return response

        except Exception as e:
            logger.error(f"Ошибка UseCase для пользователя {user_id}: {e}", exc_info=True)
            raise

    def clear_context(self, user_id: int) -> None:
        try:
            self.storage.clear_dialog(user_id)
            logger.info(f"Контекст пользователя {user_id} очищен")
        except Exception as e:
            logger.error(f"Ошибка очистки контекста для пользователя {user_id}: {e}", exc_info=True)
            raise
