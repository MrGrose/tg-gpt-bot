import logging
import sys

from bot.config import settings


class BotLogger:
    def __init__(self, name: str = "bot"):
        self.name = name
        self.is_debug = settings.DEBUG
        log_level = "DEBUG" if self.is_debug else "INFO"

        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level))
        self.logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level))
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(console_handler)
        self.info(f"Logger started, DEBUG={self.is_debug}")

    def debug(self, msg, *args, **kwargs):
        if self.is_debug:
            self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)


logger = BotLogger()
