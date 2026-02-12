from dataclasses import dataclass, field
from bot.config import settings


@dataclass
class Message:
    role: str
    content: str


@dataclass
class Dialog:
    user_id: int
    messages: list[Message] = field(default_factory=list)
    max_history: int = settings.MAX_HISTORY_MESSAGES

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role, content))
        if len(self.messages) > self.max_history * 2:
            self.messages = self.messages[-self.max_history * 2:]

    def get_context(self) -> list[dict[str, str]]:
        recent = self.messages[-self.max_history:] if self.messages else []
        return [{"role": m.role, "content": m.content} for m in recent]

    def clear(self) -> None:
        self.messages.clear()
