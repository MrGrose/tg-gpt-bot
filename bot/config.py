from pydantic_settings import BaseSettings
from pydantic import Field

SYSTEM_PROMPT = (
    "Ты полезный AI ассистент в Telegram боте.\n\n"
    "СТРОГИЕ ПРАВИЛА ФОРМАТИРОВАНИЯ:\n"
    "1. НИКОГДА не используй Markdown - никаких *, **, _, #, ```\n"
    "2. НИКОГДА не используй HTML - никаких <b>, <i>, <code>\n"
    "3. Пиши ТОЛЬКО обычным текстом\n"
    "4. Для списков используй простые дефисы: - пункт\n"
    "5. Для жирного текста используй просто заглавные буквы\n"
    "6. Отвечай кратко и по делу (1-3 предложения)\n"
    "7. На русском языке\n\n"
    "Пример правильного ответа:\n"
    "ACID - это набор свойств транзакций: Атомарность, Согласованность, Изоляция, Долговечность.\n"
    "Атомарность означает, что транзакция выполняется полностью или не выполняется вообще.\n\n"
    "НЕПРАВИЛЬНО: *ACID* - это **важный** принцип\n"
    "ПРАВИЛЬНО: ACID -ID - это важ это важный принциный принцип"
)


class Messages:
    WELCOME = "<b>Привет, {name}!</b>\n\nЯ бот консультант. Чем я могу Вам помочь?"
    NEW_DIALOG = (
        "<b>Новый диалог начат!</b>\n\nПривет, {name}! Задавай вопрос.\nЛимит: {limit} символов"
    )
    HELP = (
        "<b>Помощь по боту</b>\n\n"
        "• Отправь мне любой вопрос\n"
        "• Лимит: {limit} символов\n"
        "• Я помню до 10 сообщений\n"
        "• /start - начать новый диалог\n"
        "• /new - сброс истории диалога"
    )
    TOO_LONG = (
        "<b>Слишком длинное сообщение</b>\n\n"
        "Ты отправил: {sent} символов\n"
        "Лимит: {limit} символов\n\n"
        "Пожалуйста, сократи вопрос."
    )
    EMPTY_MESSAGE = "Пустое сообщение. Напиши что-нибудь!"
    TOO_OFTEN = "Слишком часто! Подожди секунду."
    TELEGRAM_ERROR = "Ошибка отправки сообщения."
    INTERNAL_ERROR = "Внутренняя ошибка. Попробуй /start"
    RESET_ERROR = "Ошибка при сбросе диалога."
    GENERIC_ERROR = "Произошла ошибка. Попробуй позже."
    TRUNCATED = "...\n\n[Сообщение сокращено]"


class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_USERNAME: str
    DEEPSEEK_API_KEY: str

    MAX_HISTORY_MESSAGES: int = Field(default=10, validation_alias="MAX_HISTORY_MESSAGES")
    MAX_MESSAGE_LENGTH: int = Field(default=500, validation_alias="MAX_MESSAGE_LENGTH")
    MAX_RESPONSE_LENGTH: int = Field(default=4000, validation_alias="MAX_RESPONSE_LENGTH")
    RATE_LIMIT_SECONDS: int = Field(default=1, validation_alias="RATE_LIMIT_SECONDS")
    DEBUG: bool = Field(default=False, validation_alias="DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
messages = Messages()
