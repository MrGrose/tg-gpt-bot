from bot.domain.entities import Dialog
from bot.domain.interfaces import Storage
from bot.config import settings


class MemoryStorage(Storage):
    def __init__(self):
        self._dialogs: dict[int, Dialog] = {}
        self.max_history = settings.MAX_HISTORY_MESSAGES

    def get_dialog(self, user_id: int) -> Dialog:
        if user_id not in self._dialogs:
            self._dialogs[user_id] = Dialog(user_id=user_id, max_history=self.max_history)
        return self._dialogs[user_id]

    def clear_dialog(self, user_id: int) -> None:
        if user_id in self._dialogs:
            self._dialogs[user_id].clear()
