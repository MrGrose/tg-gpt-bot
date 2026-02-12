from abc import ABC, abstractmethod
from bot.domain.entities import Dialog


class Storage(ABC):

    @abstractmethod
    def get_dialog(self, user_id: int) -> Dialog:
        pass

    @abstractmethod
    def clear_dialog(self, user_id: int) -> None:
        pass


class LLMProvider(ABC):
    @abstractmethod
    async def generate(
        self, messages: list[dict[str, str]], system_prompt: str | None = None
    ) -> str:
        pass
